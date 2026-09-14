"""Local multilingual embeddings and the maintained Neo4j hybrid retriever."""

import json
import re
import time
from functools import lru_cache

from battery_copilot.graph import graph
from battery_copilot.settings import DERIVED

MODEL = "intfloat/multilingual-e5-small"
MODEL_REVISION = "614241f622f53c4eeff9890bdc4f31cfecc418b3"
RERANKER = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
RERANKER_REVISION = "1427fd652930e4ba29e8149678df786c240d8825"


@lru_cache
def encoder():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL, revision=MODEL_REVISION, device="cpu")


@lru_cache
def reranker():
    from sentence_transformers import CrossEncoder

    return CrossEncoder(RERANKER, revision=RERANKER_REVISION, device="cpu", max_length=512)


def search(query: str, battery_id: int, scope: str = "all", limit: int = 6) -> list[dict]:
    from neo4j_graphrag.retrievers import HybridRetriever

    vector = encoder().encode("query: " + query, normalize_embeddings=True).tolist()
    # Strip Lucene operators: the UI accepts natural language, not a query language.
    terms = " ".join(re.findall(r"\w+", query, flags=re.UNICODE)) or "battery"
    retriever = HybridRetriever(
        graph().driver,
        "guide_vectors" if scope == "guide" else "evidence_vectors",
        "guide_text" if scope == "guide" else "evidence_text",
        return_properties=[
            "uid",
            "text",
            "name",
            "kind",
            "source_kind",
            "battery_id",
            "page",
            "bbox",
        ],
    )
    result = retriever.get_search_results(
        query_text=terms,
        query_vector=vector,
        top_k=100,
        effective_search_ratio=6 if scope == "guide" else 1,
    )
    rows = []
    for record in result.records:
        node = dict(record["node"])
        if node.get("source_kind") == "record" and node.get("battery_id") != battery_id:
            continue
        if scope == "guide" and node.get("source_kind") != "guide":
            continue
        rows.append({**node, "score": record["score"]})
    if scope == "guide" and rows:
        # Cross-language relevance needs the query and paragraph together; a short
        # repeated page label can otherwise outrank the actual engineering evidence.
        scores = reranker().predict([(query, r["text"]) for r in rows], batch_size=16)
        for row, score in zip(rows, scores):
            row["score"] = float(score)
        rows.sort(key=lambda r: r["score"], reverse=True)
    return rows[:limit]


def main():
    started = time.perf_counter()
    db = graph()
    db.query("MATCH (n:Searchable) REMOVE n:Searchable")
    db.query("MATCH (n:GuideChunk) REMOVE n:GuideChunk")
    db.query(
        "MATCH (n:Evidence) WHERE n.source_kind IN ['record','guide'] AND NOT n.kind IN "
        "['section_header','title','page_header','page_footer','caption'] SET n:Searchable"
    )
    rows = db.query(
        "MATCH (n:Searchable) WHERE n.embedding IS NULL RETURN n.uid AS uid,n.text AS text"
    )
    for offset in range(0, len(rows), 64):
        batch = rows[offset : offset + 64]
        vectors = encoder().encode(
            ["passage: " + r["text"] for r in batch], normalize_embeddings=True, batch_size=16
        )
        db.query(
            "UNWIND $rows AS row MATCH (n:Evidence {uid:row.uid}) SET n.embedding=row.embedding",
            rows=[
                {"uid": row["uid"], "embedding": vector.tolist()}
                for row, vector in zip(batch, vectors)
            ],
        )
        print(f"Embedded {min(offset + 64, len(rows))}/{len(rows)}", flush=True)
    db.query("MATCH (n:Searchable:Guide) SET n:GuideChunk")
    for prefix, label in [("evidence", "Searchable"), ("guide", "GuideChunk")]:
        db.query(f"DROP INDEX {prefix}_vectors IF EXISTS")
        db.query(f"DROP INDEX {prefix}_text IF EXISTS")
        db.query(
            f"CREATE VECTOR INDEX {prefix}_vectors FOR (n:{label}) ON (n.embedding) "
            "OPTIONS {indexConfig: {`vector.dimensions`:384, "
            "`vector.similarity_function`:'cosine'}}"
        )
        db.query(f"CREATE FULLTEXT INDEX {prefix}_text FOR (n:{label}) ON EACH [n.text]")
    db.query("CALL db.awaitIndexes(300)")
    reranker()  # Download during setup so the first guide query can run offline.
    DERIVED.mkdir(parents=True, exist_ok=True)
    report = {
        "model": MODEL,
        "revision": MODEL_REVISION,
        "reranker": RERANKER,
        "reranker_revision": RERANKER_REVISION,
        "dimensions": 384,
        "embedded": len(rows),
        "indexed_total": db.query("MATCH (n:Searchable) RETURN count(n) AS count")[0]["count"],
        "seconds": round(time.perf_counter() - started, 2),
    }
    (DERIVED / "embedding-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))
    db.driver.close()


if __name__ == "__main__":
    main()

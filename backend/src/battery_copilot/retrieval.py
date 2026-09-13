"""Local multilingual embeddings and the maintained Neo4j hybrid retriever."""

import json
import re
import time
from functools import lru_cache

from battery_copilot.graph import graph
from battery_copilot.settings import DERIVED

MODEL = "intfloat/multilingual-e5-small"
MODEL_REVISION = "614241f622f53c4eeff9890bdc4f31cfecc418b3"


@lru_cache
def encoder():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL, revision=MODEL_REVISION, device="cpu")


def search(query: str, battery_id: int, scope: str = "all", limit: int = 6) -> list[dict]:
    from neo4j_graphrag.retrievers import HybridRetriever

    vector = encoder().encode("query: " + query, normalize_embeddings=True).tolist()
    # Strip Lucene operators: the UI accepts natural language, not a query language.
    terms = " ".join(re.findall(r"\w+", query, flags=re.UNICODE)) or "battery"
    retriever = HybridRetriever(
        graph().driver,
        "guide_vectors" if scope == "guide" else "evidence_vectors",
        "guide_text" if scope == "guide" else "evidence_text",
        return_properties=["uid", "text", "name", "kind", "source_kind", "battery_id", "page"],
    )
    result = retriever.get_search_results(query_text=terms, query_vector=vector, top_k=100)
    rows = []
    for record in result.records:
        node = dict(record["node"])
        if node.get("source_kind") == "record" and node.get("battery_id") != battery_id:
            continue
        if scope == "guide" and node.get("source_kind") != "guide":
            continue
        rows.append({**node, "score": record["score"]})
        if len(rows) == limit:
            break
    return rows


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
    DERIVED.mkdir(parents=True, exist_ok=True)
    report = {
        "model": MODEL,
        "revision": MODEL_REVISION,
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

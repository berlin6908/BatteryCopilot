"""Frozen multilingual page and source-region retrieval checks; no answer model."""

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

from battery_copilot.graph import graph
from battery_copilot.retrieval import (
    MODEL,
    MODEL_REVISION,
    RERANKER,
    RERANKER_REVISION,
    search,
)
from battery_copilot.settings import ROOT

SUITE = ROOT / "data/guide-validation"


def coverage(target, boxes):
    """Union area inside a gold rectangle; overlapping hits must not double-count."""
    left, top, right, bottom = target
    clipped = [
        (max(left, a), max(top, b), min(right, c), min(bottom, d))
        for a, b, c, d in boxes
        if a < right and c > left and b < bottom and d > top
    ]
    boundaries = sorted({x for a, _, c, _ in clipped for x in (a, c)})
    area = 0
    for x1, x2 in zip(boundaries, boundaries[1:]):
        intervals = sorted((b, d) for a, b, c, d in clipped if a <= x1 and c >= x2)
        end, height = top, 0
        for start, stop in intervals:
            height += max(0, stop - max(end, start))
            end = max(end, stop)
        area += (x2 - x1) * height
    return area / ((right - left) * (bottom - top))


def run(output):
    if output.exists():
        raise ValueError("Use a new output file; keep prior results.")
    cases_path = SUITE / "cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    corpus = graph().query(
        "MATCH (n:Guide) RETURN n.uid AS uid,n.page AS page,n.bbox AS bbox,n.text AS text "
        "ORDER BY n.uid"
    )
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "embedding": MODEL,
        "embedding_revision": MODEL_REVISION,
        "reranker": RERANKER,
        "reranker_revision": RERANKER_REVISION,
        "candidate_top_k": 100,
        "effective_search_ratio": 6,
        "corpus_sha256": hashlib.sha256(json.dumps(corpus, sort_keys=True).encode()).hexdigest(),
        "sha256": {
            p.relative_to(ROOT).as_posix(): hashlib.sha256(
                p.read_text(encoding="utf-8").encode()
            ).hexdigest()
            for p in [
                cases_path,
                *[
                    ROOT / "backend/src/battery_copilot" / name
                    for name in [
                        "documents.py",
                        "document_sources.py",
                        "retrieval.py",
                        "guide_evaluation.py",
                    ]
                ],
                ROOT / "uv.lock",
            ]
        },
        "results": [],
    }
    for case in cases:
        started = time.perf_counter()
        hits = search(case["query"], 1, "guide", 6)
        boxes = [r["bbox"] for r in hits if r["page"] == case["page"]]
        overlaps = [round(coverage(region, boxes), 4) for region in case["regions"]]
        report["results"].append(
            {
                **case,
                "seconds": round(time.perf_counter() - started, 3),
                "page_hit_at_6": any(r["page"] == case["page"] for r in hits),
                "region_coverage": overlaps,
                "region_hit_at_6": all(v >= 0.8 for v in overlaps) if overlaps else None,
                "hits": [{k: r[k] for k in ["uid", "page", "bbox", "score"]} for r in hits],
            }
        )
    report["summary"] = [
        {
            "split": split,
            "n": len(rows),
            "page_hits": sum(r["page_hit_at_6"] for r in rows),
            "region_cases": sum(r["region_hit_at_6"] is not None for r in rows),
            "region_hits": sum(r["region_hit_at_6"] is True for r in rows),
        }
        for split in ["dev", "test"]
        for rows in [[r for r in report["results"] if r["split"] == split]]
    ]
    report["latency"] = {
        "first_query_seconds": report["results"][0]["seconds"],
        "remaining_19_median_seconds": median(r["seconds"] for r in report["results"][1:]),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output)

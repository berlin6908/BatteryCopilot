"""Small transparent evaluation, separating retrieval checks from model runs."""

import argparse
import csv
import hashlib
import json
import subprocess
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from battery_copilot.agent import SYSTEM, AgentRequest, Answer, collect_ids, model, run_agent
from battery_copilot.graph import graph
from battery_copilot.retrieval import MODEL, MODEL_REVISION, search
from battery_copilot.settings import RAW, ROOT, settings

EVAL = ROOT / "data/evaluation"


def build_cases():
    """Gold is computed directly from CSV, independently of Neo4j queries."""
    tables = {}
    for name in ("battery_catalogue", "parts", "fixations", "operations"):
        with (RAW / f"{name}.csv").open(encoding="utf-8-sig", newline="") as handle:
            tables[name] = list(csv.DictReader(handle))
    parts = {row["id"]: row for row in tables["parts"]}
    fixations = {row["id"]: row for row in tables["fixations"]}
    operation_counts = Counter(
        (parts[row["part_id"]] if row["part_id"] else fixations[row["fixation_id"]])["battery_id"]
        for row in tables["operations"]
    )
    cases = []
    for battery in tables["battery_catalogue"]:
        bid = int(battery["id"])
        cases.append(
            {
                "id": f"counts-{bid}",
                "category": "counts",
                "battery_id": bid,
                "scenario_id": "kit-v1",
                "question": f"{battery['name']} 的部件、连接件和已记录拆解操作各有多少？",
                "expected_counts": {
                    "Part": sum(r["battery_id"] == str(bid) for r in tables["parts"]),
                    "Fixation": sum(r["battery_id"] == str(bid) for r in tables["fixations"]),
                    "Operation": operation_counts[str(bid)],
                },
                "gold_basis": "Direct csv.DictReader counts, independent of the ingestion mapper",
            }
        )
        first = next(r for r in tables["fixations"] if r["battery_id"] == str(bid))
        operations = [r for r in tables["operations"] if r["fixation_id"] == first["id"]]
        expected = [f"kit-v1:part:{first[key]}" for key in ("fromPartID", "toPartID")]
        expected += [f"kit-v1:operation:{r['id']}" for r in operations]
        cases.append(
            {
                "id": f"connections-{bid}",
                "category": "connections",
                "battery_id": bid,
                "scenario_id": "kit-v1",
                "question": f"连接件 {first['id']} 连接哪些部件、对应哪条拆解操作？"
                "请引用这些对象。",
                "query": first["id"],
                "expected_ids": expected,
                "expected_names": {
                    **{
                        f"kit-v1:part:{first[k]}": parts[first[k]]["class"]
                        for k in ("fromPartID", "toPartID")
                    },
                    **{f"kit-v1:operation:{r['id']}": r["skill_id"] for r in operations},
                },
                "gold_basis": "Direct CSV references",
            }
        )
    (EVAL / "tasks.json").write_text(
        json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return cases


def run_baseline(case: dict, variant: str):
    started = time.perf_counter()
    bid = case["battery_id"]
    evidence = search(case["question"], bid, limit=12)
    if variant == "B":
        from battery_copilot.agent import read_evidence

        evidence.append(read_evidence(f"summary:{bid}", bid))
        for node in graph().entities(bid, case.get("query", ""), "Fixation", 3):
            evidence.append(graph().neighborhood(node["uid"], bid))
    fixed = create_agent(
        model(), tools=[], system_prompt=SYSTEM, response_format=ToolStrategy(Answer)
    )
    result = fixed.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": case["question"]
                    + "\n以下是固定检索结果：\n"
                    + json.dumps(evidence, ensure_ascii=False),
                }
            ]
        }
    )
    answer = result["structured_response"].model_dump()
    available = collect_ids(evidence)
    cited = {e for c in answer["claims"] for e in c["evidence_ids"]}
    usage = {"input_tokens": 0, "output_tokens": 0, "cached_input_tokens": 0, "model_calls": 0}
    for message in result["messages"]:
        metadata = getattr(message, "usage_metadata", None)
        if metadata:
            for key in ("input_tokens", "output_tokens"):
                usage[key] += metadata.get(key, 0)
            usage["cached_input_tokens"] += metadata.get("input_token_details", {}).get(
                "cache_read", 0
            )
            usage["model_calls"] += 1
    return {
        "type": "answer",
        **answer,
        "seconds": round(time.perf_counter() - started, 2),
        "usage": usage,
        "unresolved_citations": sorted(cited - available),
        "evidence": evidence,
    }


def evaluate_case(case: dict, variant: str) -> dict:
    started = time.perf_counter()
    try:
        if variant == "C":
            events = list(
                run_agent(
                    AgentRequest(**{k: case[k] for k in ("question", "battery_id", "scenario_id")})
                )
            )
            result = events[-1]
            trace = [e for e in events if e["type"] == "tool"]
            evidence = [e["result"] for e in trace if e["status"] == "completed"]
        else:
            result = run_baseline(case, variant)
            evidence, trace = result.pop("evidence"), []
    except Exception as exc:
        result = {"type": "error", "message": str(exc)}
        evidence, trace = [], []
    result.setdefault("seconds", round(time.perf_counter() - started, 2))
    cited = [e for claim in result.get("claims", []) for e in set(claim["evidence_ids"])]
    available = collect_ids(evidence)
    required = set(case.get("expected_ids", []))
    return {
        "case": case,
        "variant": variant,
        "result": result,
        "evidence": evidence,
        "trace": trace,
        "checks": {
            "returned_answer": result["type"] == "answer",
            "cited_pairs": len(cited),
            "available_cited_pairs": sum(uid in available for uid in cited),
            "unresolved_ids": sorted(set(cited) - available),
            "required_object_citations": len(required),
            "covered_object_citations": len(required & set(cited)),
        },
    }


def run_models(cases: list[dict], output: Path, variants: list[str], workers: int):
    output.mkdir(parents=True, exist_ok=False)
    files = list(RAW.glob("*.csv")) + list((ROOT / "backend/src/battery_copilot").glob("*.py"))
    files += [ROOT / "data/scenarios.json", ROOT / "uv.lock"]
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model_provider": settings().model_provider,
        "model_name": settings().model_name,
        "cli_version": subprocess.check_output(["codex", "--version"], text=True).strip()
        if settings().model_provider == "codex"
        else None,
        "embedding_model": MODEL,
        "embedding_revision": MODEL_REVISION,
        "workers": workers,
        "variants": variants,
        "case_count": len(cases),
        "repetitions": 1,
        "cases": cases,
        "sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files
        },
        "scope": "Development evaluation; code frozen during run; independent CSV reference; "
        "warm retrieval; concurrent end-to-end latency, not a model-only benchmark.",
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Warming retrieval model and indexes...", flush=True)
    search("battery module", 1, limit=1)
    jobs = [(case, variant) for case in cases for variant in variants]
    with (output / "results.jsonl").open("a", encoding="utf-8") as handle:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(evaluate_case, case, variant) for case, variant in jobs]
            for index, future in enumerate(as_completed(futures), 1):
                row = future.result()
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
                handle.flush()
                print(
                    f"{index}/{len(jobs)} {row['case']['id']} {row['variant']} "
                    f"{row['result']['type']} {row['result']['seconds']}s",
                    flush=True,
                )
    print(f"Saved {len(jobs)} attempts to {output}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["retrieval", "models", "cases"], default="retrieval")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--cases", type=Path, default=EVAL / "tasks.json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--variants", nargs="+", choices=["A", "B", "C"], default=["A", "B", "C"])
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    if args.mode == "cases":
        print(f"Generated {len(build_cases())} CSV-derived cases")
        return
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": args.mode,
        "model_provider": settings().model_provider if args.mode == "models" else None,
        "model_name": settings().model_name if args.mode == "models" else None,
        "results": [],
    }
    if args.mode == "retrieval":
        cases = json.loads((EVAL / "retrieval.json").read_text(encoding="utf-8"))
        for case in cases:
            start = time.perf_counter()
            results = search(case["query"], 1, "guide", 6)
            pages = [r["page"] for r in results]
            report["results"].append(
                {
                    **case,
                    "retrieved_pages": pages,
                    "hit_at_6": case["page"] in pages,
                    "seconds": round(time.perf_counter() - start, 3),
                }
            )
        report["hits"] = sum(r["hit_at_6"] for r in report["results"])
        report["total"] = len(cases)
        report["scope"] = "Eight development probes; page retrieval only, not answer accuracy."
    else:
        if not settings().model_ready:
            raise SystemExit("Model evaluation not run: configure the local .env first.")
        cases = json.loads(args.cases.read_text(encoding="utf-8"))[: args.limit]
        output = args.output or EVAL / (
            "terra-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        )
        run_models(cases, output, args.variants, args.workers)
        return
    (EVAL / f"{args.mode}-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in report.items() if k != "results"}, ensure_ascii=False))


if __name__ == "__main__":
    main()

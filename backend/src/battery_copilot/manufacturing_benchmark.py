"""Compare the production manufacturing Agent with a fixed dossier workflow."""

import argparse
import hashlib
import json
import math
import random
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

from langchain_core.tools import tool

from battery_copilot import manufacturing as mfg
from battery_copilot.agent import collect_ids, stream_answer
from battery_copilot.manufacturing_cases import SUITE
from battery_copilot.settings import ROOT, settings

CONTRACT = (
    "\n输出约定：把所求字段组成合法JSON对象，作为Answer.summary的完整字符串；"
    "不加代码围栏，只含题目要求的键。数字用JSON数值，布尔用true/false，缺失用null。"
    "claims仍解释并引用实际来源。整条履历或断点引用追溯结果uid，"
    "参数引用具体参数uid，循环数值引用原始行uid，文件元数据引用文件uid。"
    "没有拿到的值不要猜测。"
)


def same(actual, expected, ordered=False):
    if expected is None or isinstance(expected, bool):
        return actual is expected
    if isinstance(expected, (int, float)):
        tolerance = 0 if expected == 0 else 1e-12 if abs(expected) < 1e-6 else 5e-7
        return (
            isinstance(actual, (int, float))
            and not isinstance(actual, bool)
            and math.isclose(actual, expected, rel_tol=1e-9, abs_tol=tolerance)
        )
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            return False
        if ordered:
            return all(same(a, e, True) for a, e in zip(actual, expected))
        return Counter(json.dumps(v, sort_keys=True) for v in actual) == Counter(
            json.dumps(v, sort_keys=True) for v in expected
        )
    return type(actual) is type(expected) and actual == expected


def grade(result, gold, evidence):
    try:
        actual = json.loads(result.get("summary", ""))
    except (ValueError, TypeError):
        actual = None
    fields = {
        k: isinstance(actual, dict)
        and k in actual
        and same(actual[k], v, k in gold["ordered_fields"])
        for k, v in gold["answer"].items()
    }
    cited = {u for c in result.get("claims", []) for u in c["evidence_ids"]}
    available = collect_ids(evidence)
    required = set(gold["required_sources"])
    missing = required - cited
    answer_pass = (
        result["type"] == "answer"
        and isinstance(actual, dict)
        and set(actual) == set(gold["answer"])
        and all(fields.values())
    )
    return {
        "actual": actual,
        "fields": fields,
        "answer_pass": answer_pass,
        "answer_and_sources_pass": answer_pass and not missing and not (cited - available),
        "missing_sources": sorted(missing),
        "unresolved_sources": sorted(cited - available),
    }


def fixed_dossier(cell_uid):
    """Question-independent policy: trace, each process, first/last 12 test rows."""
    trace = mfg.trace_cell(cell_uid)
    evidence, calls = [trace], 1
    for process in sorted({s["process"]["uid"] for s in trace["stages"] if s["process"]}):
        evidence.append(mfg.process_details(cell_uid, process))
        calls += 1
    for item in trace["tests"]:
        head = mfg.test_results(cell_uid, item["test"]["uid"], 0, 12)
        evidence.append(head)
        calls += 1
        if head["row_count"] > 12:
            evidence.append(
                mfg.test_results(cell_uid, item["test"]["uid"], max(12, head["row_count"] - 12), 12)
            )
            calls += 1
    return evidence, calls


def evaluate(task, variant):
    started = time.perf_counter()
    evidence, events = [], []
    retrieval_calls = 0
    inputs = task["input"]
    question = inputs["question"] + CONTRACT
    try:
        if variant == "no_data":
            events = list(
                stream_answer(
                    f"当前电芯 {inputs['cell_uid']}。没有提供资料；未知字段不要猜。claims留空。\n"
                    + question,
                    [],
                    mfg.SYSTEM,
                    {"cell_uid": inputs["cell_uid"], "question": question, "variant": "no_data"},
                    max_model_calls=10,
                    max_tool_calls=16,
                )
            )
        elif variant == "agent":
            events = list(mfg.run_analysis(inputs["cell_uid"], question))
            retrieval_calls = sum(e["type"] == "tool" and e["status"] == "started" for e in events)
        else:
            dossier, retrieval_calls = fixed_dossier(inputs["cell_uid"])

            @tool
            def read_fixed_dossier() -> list:
                """Read the fixed manufacturing dossier; it cannot fetch additional records."""
                return dossier

            events = list(
                stream_answer(
                    f"当前电芯 {inputs['cell_uid']}。先调用read_fixed_dossier读取档案，再回答。\n"
                    + question,
                    [read_fixed_dossier],
                    mfg.SYSTEM,
                    {"cell_uid": inputs["cell_uid"], "question": question, "variant": "fixed"},
                    max_model_calls=10,
                    max_tool_calls=16,
                )
            )
        result = events[-1]
        evidence = [
            e["result"] for e in events if e["type"] == "tool" and e["status"] == "completed"
        ]
    except Exception as exc:
        result = {"type": "error", "message": str(exc)}
    return {
        "case_id": task["id"],
        "split": task["split"],
        "batch": task["batch"],
        "category": task["category"],
        "variant": variant,
        "seconds": round(time.perf_counter() - started, 2),
        "retrieval_calls": retrieval_calls,
        "result": result,
        "events": events,
        "score": grade(result, task["gold"], evidence),
    }


def summarize(directory):
    rows = [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted((directory / "attempts").glob("*.json"))
    ]
    summary = {"attempts": len(rows), "groups": []}
    for split in ("dev", "test"):
        for variant in ("no_data", "fixed", "agent"):
            selected = [r for r in rows if r["split"] == split and r["variant"] == variant]
            if not selected:
                continue
            group = {
                "split": split,
                "variant": variant,
                "attempts": len(selected),
                "answer_pass": sum(r["score"]["answer_pass"] for r in selected),
                "answer_and_sources_pass": sum(
                    r["score"]["answer_and_sources_pass"] for r in selected
                ),
                "median_seconds": round(median(r["seconds"] for r in selected), 2),
                "retrieval_calls": sum(r["retrieval_calls"] for r in selected),
                "usage": {
                    key: sum(r["result"].get("usage", {}).get(key, 0) for r in selected)
                    for key in (
                        "input_tokens",
                        "output_tokens",
                        "cached_input_tokens",
                        "model_calls",
                    )
                },
                "categories": {},
                "failures": [],
            }
            for category in sorted({r["category"] for r in selected}):
                subset = [r for r in selected if r["category"] == category]
                group["categories"][category] = {
                    "n": len(subset),
                    "answer_pass": sum(r["score"]["answer_pass"] for r in subset),
                    "answer_and_sources_pass": sum(
                        r["score"]["answer_and_sources_pass"] for r in subset
                    ),
                }
            group["failures"] = [
                {"id": r["case_id"], "score": r["score"], "error": r["result"].get("message")}
                for r in selected
                if not r["score"]["answer_and_sources_pass"]
            ]
            summary["groups"].append(group)
    (directory / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "attempts": len(rows),
                "groups": [
                    {k: v for k, v in g.items() if k not in ("categories", "failures")}
                    for g in summary["groups"]
                ],
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--split", choices=("dev", "test", "all"), default="all")
    parser.add_argument(
        "--variants",
        nargs="+",
        choices=("no_data", "fixed", "agent"),
        default=["no_data", "fixed", "agent"],
    )
    parser.add_argument("--workers", type=int, choices=range(1, 5), default=3)
    parser.add_argument("--summarize", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.summarize:
        summarize(args.output)
        return
    cases = json.loads((SUITE / "cases.json").read_text(encoding="utf-8"))
    config = {
        "model": settings().model_name,
        "provider": settings().model_provider,
        "workers": args.workers,
        "variants": args.variants,
        "max_model_calls": 10,
        "max_tool_calls": 16,
        "sha256": {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [
                *sorted((ROOT / "backend/src/battery_copilot").glob("*.py")),
                SUITE / "cases.json",
                SUITE / "manifest.json",
                ROOT / "uv.lock",
            ]
        },
    }
    manifest_path = args.output / "manifest.json"
    if manifest_path.exists():
        if json.loads(manifest_path.read_text(encoding="utf-8"))["config"] != config:
            raise ValueError("Frozen source/config changed; use a new output directory")
    else:
        manifest_path.write_text(
            json.dumps(
                {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "config": config,
                    "suite_cases": len(cases),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    attempts = args.output / "attempts"
    attempts.mkdir(exist_ok=True)
    jobs = [
        (c, v)
        for c in cases
        if args.split == "all" or c["split"] == args.split
        for v in args.variants
        if not (attempts / f"{c['id']}-{v}.json").exists()
    ]
    random.Random(20260914).shuffle(jobs)
    print(f"Running {len(jobs)} frozen attempts", flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(evaluate, c, v) for c, v in jobs]
        for i, future in enumerate(as_completed(futures), 1):
            row = future.result()
            path = attempts / f"{row['case_id']}-{row['variant']}.json"
            temporary = path.with_suffix(".tmp")
            temporary.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
            temporary.replace(path)
            print(
                f"{i}/{len(jobs)} {row['case_id']} {row['variant']} "
                f"answer={row['score']['answer_pass']} "
                f"sources={row['score']['answer_and_sources_pass']} "
                f"{row['seconds']}s",
                flush=True,
            )
    summarize(args.output)


if __name__ == "__main__":
    main()

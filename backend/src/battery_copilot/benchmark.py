"""Run and score the frozen 300-case suite with the production Agent and two controls."""

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

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.messages import AIMessage

from battery_copilot.agent import (
    SYSTEM,
    AgentRequest,
    Answer,
    collect_ids,
    model,
    read_evidence,
    run_agent,
)
from battery_copilot.benchmark_cases import CATEGORIES, SUITE
from battery_copilot.cases import build_context
from battery_copilot.graph import graph
from battery_copilot.retrieval import MODEL, MODEL_REVISION, search
from battery_copilot.settings import ROOT, settings

MODEL_CALLS = 8
TOOL_CALLS = 12
CONTRACT = (
    "\n输出约定：将所求字段组成一个合法 JSON 对象，作为 Answer.summary 的完整字符串内容；"
    "不要添加 Markdown 代码围栏或 JSON 以外的文字。只包含题目要求的键。"
    "数值使用 JSON 数字，布尔值用 true/false，缺失值用 null。"
    "UID 保持原样，类别和部件编号保持源记录原文。claims 用中文解释并引用实际证据，"
    "unknowns 记录未解决项。不得猜测缺失事实。"
)


def prompt(inputs, values=None):
    text = inputs["question"]
    text += "\n当前产品及查询线索：" + json.dumps(
        {k: inputs[k] for k in ["battery_id", "anchors", "search_query", "guide_page"]},
        ensure_ascii=False,
    )
    if values:
        text += "\n当前模拟变更输入：" + json.dumps(values, ensure_ascii=False)
        text += (
            "\n资料缺失时状态为 awaiting_information，否则为 awaiting_review。"
            "全部规则通过后才可由人工逐项复核并完成。"
        )
    return text + CONTRACT


def fixed_evidence(inputs, variant, context):
    """A retrieval; B a declared fixed workflow. No family names or gold enter here."""
    evidence, trace = [], []
    bid = inputs["battery_id"]

    def call(name, args, action):
        if len(trace) >= TOOL_CALLS:
            return None
        try:
            result = action()
        except ValueError as exc:
            result = {"error": str(exc)}
        trace.append(
            {"type": "tool", "status": "completed", "name": name, "args": args, "result": result}
        )
        evidence.append(result)
        return result

    scope = "guide" if inputs["guide_page"] else "all"
    call(
        "search_evidence",
        {"query": inputs["search_query"], "scope": scope, "limit": 12},
        lambda: search(inputs["search_query"], bid, scope, 12),
    )
    if context:
        # All variants have access to the same supplied application documents.
        evidence.extend(s for s in context["evidence"] if s["source_kind"] == "simulation")
    if variant == "A":
        return evidence, trace
    if context:
        call("compare_change", {}, lambda: context)
    if inputs["guide_page"]:
        # The existing document-page API is the fixed workflow's page lookup.
        call(
            "document_elements",
            {"page": inputs["guide_page"]},
            lambda: [
                r["node"]
                for r in graph().query(
                    "MATCH (n:Guide {page:$page}) "
                    "RETURN n{.*,embedding:null} AS node ORDER BY n.uid",
                    page=inputs["guide_page"],
                )
            ],
        )
    else:
        call("summarize_records", {}, lambda: read_evidence(f"summary:{bid}", bid))
        for anchor in inputs["anchors"]:
            node = call(
                "read_source", {"evidence_id": anchor}, lambda a=anchor: read_evidence(a, bid)
            )
            if not node or "error" in node or node.get("kind") == "Battery":
                continue
            local = call(
                "trace_relations", {"uid": anchor}, lambda a=anchor: graph().neighborhood(a, bid)
            )
            call(
                "get_recorded_sequence",
                {"target_uid": anchor},
                lambda a=anchor: graph().sequence(bid, 0, 15, a),
            )
            # A fixed second expansion on up to two directly connected objects.
            for neighbor in (local or {}).get("nodes", [])[1:3]:
                call(
                    "trace_relations",
                    {"uid": neighbor["uid"]},
                    lambda n=neighbor: graph().neighborhood(n["uid"], bid),
                )
    return evidence, trace


def run_fixed(inputs, variant, values, context):
    started = time.perf_counter()
    usage = {"input_tokens": 0, "output_tokens": 0, "cached_input_tokens": 0, "model_calls": 0}
    evidence, trace = fixed_evidence(inputs, variant, context)
    answer = None
    try:
        agent = create_agent(
            model(), tools=[], system_prompt=SYSTEM, response_format=ToolStrategy(Answer)
        )
        messages = [
            {
                "role": "user",
                "content": prompt(inputs, values)
                + "\n固定工作流已返回下列证据，按这些证据作答：\n"
                + json.dumps(evidence, ensure_ascii=False),
            }
        ]
        for update in agent.stream(
            {"messages": messages}, {"recursion_limit": MODEL_CALLS * 2 + 1}, stream_mode="updates"
        ):
            for state in update.values():
                if state is None:
                    continue
                if state.get("structured_response"):
                    answer = state["structured_response"].model_dump()
                for message in state.get("messages", []):
                    if isinstance(message, AIMessage):
                        metadata = message.usage_metadata or {}
                        for key in ["input_tokens", "output_tokens"]:
                            usage[key] += metadata.get(key, 0)
                        usage["cached_input_tokens"] += metadata.get("input_token_details", {}).get(
                            "cache_read", 0
                        )
                        usage["model_calls"] += 1
                if answer is None and usage["model_calls"] >= MODEL_CALLS:
                    raise ValueError("Model-call budget exhausted before a complete answer.")
        if answer is None:
            raise ValueError("No structured answer")
        result = {"type": "answer", **answer}
    except Exception as exc:
        result = {"type": "error", "message": str(exc)}
    result.update(seconds=round(time.perf_counter() - started, 2), usage=usage)
    return result, evidence, trace


def canonical(value, ordered=False):
    if isinstance(value, dict):
        return {key: canonical(item, ordered) for key, item in sorted(value.items())}
    if isinstance(value, list):
        items = [canonical(item, ordered) for item in value]
        return (
            items if ordered else sorted(items, key=lambda item: json.dumps(item, sort_keys=True))
        )
    return value.strip() if isinstance(value, str) else value


def same(actual, expected, ordered=False):
    return json.dumps(canonical(actual, ordered), sort_keys=True) == json.dumps(
        canonical(expected, ordered), sort_keys=True
    )


def grade(result, gold, evidence):
    try:
        actual = json.loads(result.get("summary", ""))
        if not isinstance(actual, dict):
            raise ValueError("Expected a JSON object")
    except (ValueError, TypeError):
        actual = None
    expected = gold["answer"]
    fields = {
        key: actual is not None
        and key in actual
        and same(actual[key], value, key in gold["ordered_fields"])
        for key, value in expected.items()
    }
    cited = {uid for claim in result.get("claims", []) for uid in claim["evidence_ids"]}
    available = collect_ids(evidence)
    required = set(gold["required_sources"])
    covered = set(required & cited)
    for source, alternatives in gold.get("source_alternatives", {}).items():
        if set(alternatives).issubset(cited):
            covered.add(source)
    exact = (
        result["type"] == "answer"
        and actual is not None
        and set(actual) == set(expected)
        and all(fields.values())
    )
    return {
        "parseable": actual is not None,
        "actual": actual,
        "field_correct": fields,
        "answer_correct": exact,
        "required_sources": len(required),
        "covered_sources": len(covered),
        "unresolved_citations": sorted(cited - available),
        "cited_sources": len(cited),
        "grounded_task_pass": exact and covered == required and not (cited - available),
    }


def evaluate(task, variant):
    started = time.perf_counter()
    steps = []
    for index, stage in enumerate(task.get("steps", [{"input": None, "gold": task["gold"]}]), 1):
        context, evidence, trace = None, [], []
        try:
            if stage["input"]:
                context = build_context(
                    {"id": task["id"], "input_version": index, "input": stage["input"]}
                )
            if variant == "C":
                events = list(
                    run_agent(
                        AgentRequest(
                            battery_id=task["input"]["battery_id"],
                            question=prompt(task["input"], stage["input"]),
                        ),
                        case_context=context,
                        max_model_calls=MODEL_CALLS,
                        max_tool_calls=TOOL_CALLS,
                    )
                )
                result = events[-1]
                trace = [e for e in events if e["type"] in ["tool", "validation"]]
                evidence = [
                    e["result"] for e in trace if e["type"] == "tool" and e["status"] == "completed"
                ]
            else:
                result, evidence, trace = run_fixed(task["input"], variant, stage["input"], context)
        except Exception as exc:
            result = {"type": "error", "message": str(exc)}
        steps.append(
            {
                "stage": index,
                "result": result,
                "evidence": evidence,
                "trace": trace,
                "score": grade(result, stage["gold"], evidence),
            }
        )
    return {
        "case_id": task["id"],
        "category": task["category"],
        "family": task["family"],
        "split": task["split"],
        "variant": variant,
        "steps": steps,
        "returned_answer": all(s["result"]["type"] == "answer" for s in steps),
        "answer_correct": all(s["score"]["answer_correct"] for s in steps),
        "grounded_task_pass": all(s["score"]["grounded_task_pass"] for s in steps),
        "seconds": round(time.perf_counter() - started, 2),
    }


def fingerprint():
    files = [
        *sorted((ROOT / "backend/src/battery_copilot").glob("*.py")),
        SUITE / "cases.json",
        ROOT / "uv.lock",
        *sorted((ROOT / "data/sources/kit-battery").glob("*.csv")),
        DERIVED_PATH,
    ]
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


DERIVED_PATH = ROOT / "data/derived/pem/elements.json"


def run(args):
    tasks = json.loads((SUITE / "cases.json").read_text(encoding="utf-8"))
    selected = [
        t
        for t in tasks
        if (args.split == "all" or t["split"] == args.split)
        and (not args.ids or t["id"] in args.ids)
    ]
    if args.limit:
        selected = selected[: args.limit]
    if any(t["category"] == "guide" for t in selected):
        annotations = json.loads((SUITE / "guide-annotations.json").read_text(encoding="utf-8"))
        digest = hashlib.sha256(DERIVED_PATH.read_text(encoding="utf-8").encode()).hexdigest()
        if digest != annotations["elements_sha256"]:
            raise ValueError(
                "Guide parser snapshot differs from the frozen annotations. "
                "Use the original parsed snapshot or independently re-annotate a new suite; "
                "do not score the historical guide IDs against a fresh parse. "
                "See docs/benchmark-300.md."
            )
    config = {
        "model": settings().model_name,
        "provider": settings().model_provider,
        "embedding": MODEL,
        "embedding_revision": MODEL_REVISION,
        "model_calls_per_stage": MODEL_CALLS,
        "tool_calls_per_stage": TOOL_CALLS,
        "sha256": fingerprint(),
        "workers": args.workers,
        "variants": args.variants,
    }
    args.output.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output / "manifest.json"
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        if previous["config"] != config:
            raise ValueError(
                "Run fingerprint changed; use a new output directory instead of mixing results."
            )
    else:
        manifest_path.write_text(
            json.dumps(
                {
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "config": config,
                    "suite_cases": 300,
                    "repetitions": 1,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    attempts = args.output / "attempts"
    attempts.mkdir(exist_ok=True)
    search("battery module", 1, limit=1)
    jobs = [
        (task, variant)
        for task in selected
        for variant in args.variants
        if not (attempts / f"{task['id']}-{variant}.json").exists()
    ]
    random.Random(20260913).shuffle(jobs)
    print(
        f"Pending {len(jobs)} attempts; {len(selected)} selected cases; model {config['model']}",
        flush=True,
    )
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(evaluate, task, variant) for task, variant in jobs]
        for index, future in enumerate(as_completed(futures), 1):
            row = future.result()
            path = attempts / f"{row['case_id']}-{row['variant']}.json"
            temporary = path.with_suffix(".tmp")
            temporary.write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
            temporary.replace(path)
            print(
                f"{index}/{len(jobs)} {row['case_id']} {row['variant']} "
                f"answer={row['answer_correct']} grounded={row['grounded_task_pass']} "
                f"{row['seconds']}s",
                flush=True,
            )
    summarize(args.output)


def summarize(directory):
    rows = [
        json.loads(p.read_text(encoding="utf-8"))
        for p in sorted((directory / "attempts").glob("*.json"))
    ]
    summary = {"attempts": len(rows), "by_split": {}}
    for split in ["dev", "test"]:
        summary["by_split"][split] = {}
        for variant in ["A", "B", "C"]:
            selected = [r for r in rows if r["split"] == split and r["variant"] == variant]
            if not selected:
                continue
            n = len(selected)
            usage = [
                s["result"]["usage"] for r in selected for s in r["steps"] if "usage" in s["result"]
            ]
            latencies = sorted(r["seconds"] for r in selected)
            summary["by_split"][split][variant] = {
                "attempts": n,
                "answers": sum(r["returned_answer"] for r in selected),
                "answer_correct": sum(r["answer_correct"] for r in selected),
                "grounded_task_pass": sum(r["grounded_task_pass"] for r in selected),
                "median_seconds": round(median(latencies), 2),
                "p95_seconds": latencies[math.ceil(0.95 * n) - 1],
                "observed_usage": {
                    k: sum(u.get(k, 0) for u in usage)
                    for k in ["input_tokens", "output_tokens", "cached_input_tokens", "model_calls"]
                },
                "steps_with_usage": len(usage),
                "steps": sum(len(r["steps"]) for r in selected),
                "categories": {
                    c: {
                        "attempts": sum(r["category"] == c for r in selected),
                        "answer_correct": sum(
                            r["category"] == c and r["answer_correct"] for r in selected
                        ),
                        "grounded_task_pass": sum(
                            r["category"] == c and r["grounded_task_pass"] for r in selected
                        ),
                    }
                    for c in CATEGORIES
                },
                "errors": dict(
                    Counter(
                        s["result"].get("message", "")[:160]
                        for r in selected
                        for s in r["steps"]
                        if s["result"]["type"] == "error"
                    )
                ),
            }
    (directory / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--split", choices=["dev", "test", "all"], default="all")
    parser.add_argument("--ids", nargs="+")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--variants", nargs="+", choices=["A", "B", "C"], default=["A", "B", "C"])
    parser.add_argument("--workers", type=int, choices=range(1, 7), default=4)
    parser.add_argument("--summarize", action="store_true")
    args = parser.parse_args()
    if args.summarize:
        summarize(args.output)
    else:
        run(args)


if __name__ == "__main__":
    main()

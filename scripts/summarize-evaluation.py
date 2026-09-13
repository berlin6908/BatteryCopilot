"""Aggregate a completed run after explicit per-answer source review."""

import argparse
import json
import math
from pathlib import Path
from statistics import mean, median


def ratio(numerator, denominator):
    return round(numerator / denominator, 4) if denominator else None


def summarize(directory):
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    rows = [
        json.loads(line)
        for line in (directory / "results.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    review = json.loads((directory / "review.json").read_text(encoding="utf-8"))
    decisions = {(r["case_id"], r["variant"]): r for r in review["items"]}
    expected = {(c["id"], v) for c in manifest["cases"] for v in manifest["variants"]}
    actual = {(r["case"]["id"], r["variant"]) for r in rows}
    assert len(rows) == len(actual) and actual == expected == set(decisions), (
        "Incomplete run/review"
    )
    summary = {"run": directory.name, "reviewer": review["reviewer"], "variants": {}}
    for variant in manifest["variants"]:
        selected = [r for r in rows if r["variant"] == variant]
        annotations = [decisions[(r["case"]["id"], variant)] for r in selected]
        for row, note in zip(selected, annotations):
            assert len(note["claims_supported"]) == len(row["result"].get("claims", []))
            assert not note["task_pass"] or row["checks"]["returned_answer"]
        answers = [r for r in selected if r["checks"]["returned_answer"]]
        successful_usage = [r["result"]["usage"] for r in answers if "usage" in r["result"]]
        observed_usage = [r["result"]["usage"] for r in selected if "usage" in r["result"]]
        supported = sum(sum(n["claims_supported"]) for n in annotations)
        claims = sum(len(n["claims_supported"]) for n in annotations)
        valid = sum(r["checks"]["available_cited_pairs"] for r in selected)
        cited = sum(r["checks"]["cited_pairs"] for r in selected)
        covered = sum(r["checks"]["covered_object_citations"] for r in selected)
        required = sum(r["checks"]["required_object_citations"] for r in selected)
        passed = sum(n["task_pass"] for n in annotations)
        latencies = sorted(r["result"]["seconds"] for r in selected)
        totals = {
            k: sum(u.get(k, 0) for u in observed_usage)
            for k in ("input_tokens", "output_tokens", "cached_input_tokens", "model_calls")
        }
        summary["variants"][variant] = {
            "attempts": len(selected),
            "answers": len(answers),
            "execution_success_rate": ratio(len(answers), len(selected)),
            "task_passes": passed,
            "task_complete_correct_rate": ratio(passed, len(selected)),
            "supported_claims": supported,
            "claims": claims,
            "claim_support_rate": ratio(supported, claims),
            "valid_citation_pairs": valid,
            "citation_pairs": cited,
            "citation_id_validity": ratio(valid, cited),
            "covered_required_objects": covered,
            "required_objects": required,
            "required_object_citation_recall": ratio(covered, required),
            "median_seconds": round(median(latencies), 2),
            "p95_seconds": latencies[math.ceil(len(latencies) * 0.95) - 1],
            "mean_input_tokens_per_answer": round(
                mean(u["input_tokens"] for u in successful_usage), 1
            )
            if successful_usage
            else None,
            "mean_model_calls_per_answer": round(
                mean(u["model_calls"] for u in successful_usage), 2
            )
            if successful_usage
            else None,
            "usage_observed": totals,
            "attempts_with_usage": len(observed_usage),
            "cached_fraction_of_observed_input": ratio(
                totals["cached_input_tokens"], totals["input_tokens"]
            ),
        }
    (directory / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directories", nargs="+", type=Path)
    for directory in parser.parse_args().directories:
        print(json.dumps(summarize(directory), ensure_ascii=False, indent=2))

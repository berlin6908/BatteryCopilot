import json
import runpy

from battery_copilot.evaluate import evaluate_case
from battery_copilot.settings import ROOT


def test_evaluation_keeps_errors_and_separates_citation_coverage_from_validity(monkeypatch):
    case = {"id": "probe", "expected_ids": ["row:2"]}
    monkeypatch.setattr(
        "battery_copilot.evaluate.run_baseline",
        lambda *args: {
            "type": "answer",
            "claims": [{"statement": "value", "evidence_ids": ["row:2"]}],
            "evidence": [{"uid": "row:1", "text": "row:2 mentioned but not retrieved"}],
        },
    )
    row = evaluate_case(case, "A")
    assert row["checks"]["covered_object_citations"] == 1
    assert row["checks"]["available_cited_pairs"] == 0
    assert row["checks"]["unresolved_ids"] == ["row:2"]

    def unavailable(*args):
        raise RuntimeError("service unavailable")

    monkeypatch.setattr("battery_copilot.evaluate.run_baseline", unavailable)
    row = evaluate_case(case, "A")
    assert not row["checks"]["returned_answer"]
    assert row["result"]["message"] == "service unavailable"


def test_summary_keeps_failed_attempts_and_missing_usage(tmp_path):
    summarize = runpy.run_path(str(ROOT / "scripts/summarize-evaluation.py"))["summarize"]
    manifest = {"cases": [{"id": "pass"}, {"id": "error"}], "variants": ["C"]}
    rows, notes = [], []
    for case_id, passed, seconds in [("pass", True, 10), ("error", False, 20)]:
        result = {"seconds": seconds, "claims": [{}] if passed else []}
        if passed:
            result["usage"] = {
                "input_tokens": 100,
                "output_tokens": 10,
                "cached_input_tokens": 50,
                "model_calls": 2,
            }
        rows.append(
            {
                "case": {"id": case_id},
                "variant": "C",
                "result": result,
                "checks": {
                    "returned_answer": passed,
                    "available_cited_pairs": int(passed),
                    "cited_pairs": int(passed),
                    "covered_object_citations": int(passed),
                    "required_object_citations": 1,
                },
            }
        )
        notes.append(
            {
                "case_id": case_id,
                "variant": "C",
                "task_pass": passed,
                "claims_supported": [True] if passed else [],
            }
        )
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    (tmp_path / "review.json").write_text(json.dumps({"reviewer": "test", "items": notes}))
    (tmp_path / "results.jsonl").write_text("\n".join(map(json.dumps, rows)))
    summary = summarize(tmp_path)["variants"]["C"]
    assert summary["task_complete_correct_rate"] == 0.5
    assert summary["required_object_citation_recall"] == 0.5
    assert summary["mean_input_tokens_per_answer"] == 100
    assert summary["attempts_with_usage"] == 1

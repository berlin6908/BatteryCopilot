import json

import pytest
from battery_copilot.benchmark import grade, prompt
from battery_copilot.benchmark_cases import SUITE, SourceRows, build


def test_scoring_requires_correct_values_order_and_retrieved_sources():
    gold = {
        "answer": {"operations": ["a", "b"], "documented": True},
        "ordered_fields": ["operations"],
        "required_sources": ["row:1"],
    }
    result = {
        "type": "answer",
        "summary": json.dumps(gold["answer"]),
        "claims": [{"evidence_ids": ["row:1"]}],
    }
    evidence = [{"uid": "row:1"}]
    assert grade(result, gold, evidence)["grounded_task_pass"]
    assert not grade(result, gold, [])["grounded_task_pass"]
    for answer in [
        {"operations": ["b", "a"], "documented": True},
        {"operations": ["a", "b"], "documented": 1},
        {"operations": ["a", "b"], "documented": True, "extra": 0},
    ]:
        assert not grade(dict(result, summary=json.dumps(answer)), gold, evidence)["answer_correct"]
    assert not grade(dict(result, claims=[]), gold, evidence)["grounded_task_pass"]


def test_complete_record_citations_can_support_aggregate_but_partial_cannot():
    gold = {
        "answer": {"screw": 2},
        "ordered_fields": [],
        "required_sources": ["summary:1"],
        "source_alternatives": {"summary:1": ["row:1", "row:2"]},
    }
    result = {"type": "answer", "summary": '{"screw":2}'}
    evidence = [{"uid": "row:1"}, {"uid": "row:2"}]
    for refs, expected in [(["row:1"], False), (["row:1", "row:2"], True)]:
        scored = grade(dict(result, claims=[{"evidence_ids": refs}]), gold, evidence)
        assert scored["grounded_task_pass"] is expected


def test_frozen_cases_reproduce_and_keep_sources_inside_product_scope():
    frozen = json.loads((SUITE / "cases.json").read_text(encoding="utf-8"))
    assert build() == frozen
    oracle = SourceRows()
    for task in frozen:
        for source in task["sources"]:
            if not source["uid"].startswith("kit-v1:"):
                continue
            row = oracle.by_uid[source["uid"]]
            assert source["line"] == row["source_line"]
            assert int(row.get("battery_id", row["id"])) == task["input"]["battery_id"]
        for stage in task.get("steps", [{"input": None}]):
            assert len(prompt(task["input"], stage["input"])) <= 4000
        if task["category"] == "workflow":
            assert oracle.by_uid[task["input"]["anchors"][0]]["class"] == "screw"


@pytest.mark.parametrize("field", ["operations", "sources"])
def test_unordered_sets_allow_permutation_without_dropping_duplicates(field):
    gold = {"answer": {field: ["a", "b"]}, "ordered_fields": [], "required_sources": []}
    result = {"type": "answer", "claims": [], "summary": json.dumps({field: ["b", "a"]})}
    assert grade(result, gold, [])["answer_correct"]
    result["summary"] = json.dumps({field: ["a", "b", "b"]})
    assert not grade(result, gold, [])["answer_correct"]

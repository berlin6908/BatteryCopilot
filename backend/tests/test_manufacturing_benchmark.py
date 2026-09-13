import json

from battery_copilot.manufacturing_benchmark import grade, requested_cycles, same
from battery_copilot.manufacturing_cases import SUITE


def test_scoring_separates_missing_zero_rounding_and_evidence():
    assert not same(0, 5.7651e-8)
    assert not same(5.7651e-8, 0)
    gold = {
        "answer": {"charge": None, "dcir": 0, "capacity": 0.438290, "accepted": False},
        "ordered_fields": [],
        "required_sources": ["file:L11"],
    }
    answer = {
        "type": "answer",
        "summary": json.dumps(
            {"charge": None, "dcir": 0.0, "capacity": 0.438290374336, "accepted": False}
        ),
        "claims": [{"evidence_ids": ["file:L11"]}],
    }
    assert grade(answer, gold, [{"uid": "file:L11"}])["answer_and_sources_pass"]
    for field, value in [("charge", 0), ("dcir", None), ("accepted", 0), ("capacity", 0.4383)]:
        wrong = json.loads(answer["summary"])
        wrong[field] = value
        assert not grade({**answer, "summary": json.dumps(wrong)}, gold, [])["answer_pass"]
    assert not grade(answer, gold, [])["answer_and_sources_pass"]


def test_fixed_query_selects_cycles_from_question_not_file_dates_or_output_keys():
    assert requested_cycles("Cycle 1 和 Cycle 100，输出cycle1_ah，文件230306-0100.txt") == [1, 100]
    assert requested_cycles("核对循环0及循环 50") == [0, 50]
    assert requested_cycles("核对2023年文件末尾12行") == []


def test_source_checked_cases_keep_batches_separate_and_cover_counterexamples():
    cases = json.loads((SUITE / "cases.json").read_text(encoding="utf-8"))
    dev = {c["batch"] for c in cases if c["split"] == "dev"}
    test = {c["batch"] for c in cases if c["split"] == "test"}
    assert not dev & test
    assert len(dev) == 2 and len(test) == 10
    assert cases[0]["gold"]["answer"]["chain"] == ["DryCell", "FilledCell1", "FormatedCell1"]
    assert cases[6]["gold"]["answer"]["unique_processes"] == 3
    assert len(cases[6]["gold"]["answer"]["chain"]) == 4
    assert cases[7]["gold"]["answer"]["linked_object_count"] == 2
    assert cases[30]["gold"]["answer"] == {
        "wet_g": 2.27,
        "dry_with_bracing_g": None,
        "can_compute_mass_difference": False,
    }

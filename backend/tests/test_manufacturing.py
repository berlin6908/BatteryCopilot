"""Numerical parsing and actual KIproBatt object-to-test provenance contracts."""

import json
import uuid

import pytest
from battery_copilot import manufacturing as mfg
from battery_copilot.graph import graph
from battery_copilot.manufacturing_ingest import BASE, parse_stats, uid

CELL = uid(BASE + "LabObject-3AOSL9f61349f3b81400b9f4049ac95e03cd7-23O0001")
SIBLING = uid(BASE + "LabObject-3AOSL9f61349f3b81400b9f4049ac95e03cd7-23O0002")


def test_maccor_preserves_empty_values_scientific_notation_and_source_lines():
    data = parse_stats(
        "Channel Number:\t59\n\nCycle\tAH-IN\tAH-OUT\tDate\n"
        "0\t\t1,12544E-7\t45007,61049\n1\t0,5153\t0,43829\t45008,12\n",
        "test",
    )
    assert data["rows"][0]["values"]["AH-IN"] is None
    assert data["rows"][0]["values"]["AH-OUT"] == pytest.approx(1.12544e-7)
    assert data["rows"][1]["values"]["AH-OUT"] == pytest.approx(0.43829)
    assert data["rows"][1]["uid"] == "test:L5"
    assert data["rows"][1]["raw"]["AH-OUT"] == "0,43829"


@pytest.fixture
def imported():
    if not graph().query("MATCH (d:MfgDataset) RETURN d.uid AS uid"):
        pytest.skip("Requires imported KIproBatt v0.3.2")


@pytest.mark.integration
def test_real_lineage_stops_at_missing_link_and_excludes_batch_siblings(imported):
    catalogue = mfg.catalogue()
    assert len(catalogue["cells"]) == catalogue["dataset"]["test_linked_objects"] == 109
    assert catalogue["dataset"]["linked_stats_files"] == 108
    trace = mfg.trace_cell(CELL)
    assert [s["object"]["name"] for s in trace["stages"]] == [
        "DryCell",
        "FilledCell1",
        "FormatedCell1",
    ]
    assert SIBLING not in {s["object"]["uid"] for s in trace["stages"]}
    assert len(trace["links"]) == 2
    snapshot = json.loads(mfg.read_source(CELL, trace["uid"])["raw_record"])
    assert snapshot["trace_endpoints"] == [trace["stages"][0]["object"]["uid"]]
    formation = next(s["process"] for s in trace["stages"] if s["object"]["uid"] == CELL)
    parameters = [
        p for s in mfg.process_details(CELL, formation["uid"])["steps"] for p in s["parameters"]
    ]
    by_name = {p["name"]: p for p in parameters}
    assert by_name["MeasurementChannel1"]["values"] == ["59"]
    assert by_name["CompactingPressure1"]["values"] == []
    assert "MeasurementChannel2" not in by_name
    with pytest.raises(ValueError, match="可追溯范围"):
        mfg.read_source(CELL, SIBLING)


@pytest.mark.integration
def test_linked_cycle_row_matches_original_export_and_rejects_foreign_cell(imported):
    test_uid = mfg.trace_cell(CELL)["tests"][0]["test"]["uid"]
    result = mfg.test_results(CELL, test_uid, 1, 1)
    row = result["rows"][0]
    assert row["values"]["Cycle"] == 1
    assert row["values"]["AH-OUT"] == pytest.approx(0.438290374336)
    source = mfg.read_source(CELL, row["uid"])
    assert "0,438290374336" in source["raw_record"]
    assert source["source_line"] == row["source_line"]
    with pytest.raises(ValueError, match="未关联"):
        mfg.test_data(SIBLING, test_uid)


@pytest.mark.integration
def test_saved_report_preserves_evidence_and_manual_review(imported, monkeypatch):
    report_id = "test-" + uuid.uuid4().hex
    test_uid = mfg.trace_cell(CELL)["tests"][0]["test"]["uid"]
    row = mfg.test_results(CELL, test_uid, 1, 1)["rows"][0]
    answer = {
        "type": "answer",
        "run_id": report_id,
        "summary": "循环1记录复核",
        "claims": [
            {
                "statement": "循环1放电容量为0.438290374336 Ah。",
                "scope": "record",
                "evidence_ids": [row["uid"]],
            }
        ],
        "unknowns": ["缺少验收标准"],
        "next_actions": ["核对测试程序"],
    }
    monkeypatch.setattr(mfg, "stream_answer", lambda *a, **kw: iter([answer]))
    try:
        result = list(mfg.run_report(CELL, "读取循环1"))[-1]
        report = mfg.get_report(result["report_id"])
        assert report["review"] is None
        assert report["evidence"][row["uid"]]["source_line"] == row["source_line"]
        reviewed = mfg.review_report(report_id, "automated test", "needs_information", "补测试条件")
        assert "补测试条件" in mfg.export_report(reviewed)
        assert "0,438290374336" in mfg.export_report(reviewed)
        with pytest.raises(ValueError, match="已复核"):
            mfg.review_report(report_id, "automated test", "verified", "重复提交")
    finally:
        graph().query("MATCH (r:MfgReport {uid:$id}) DETACH DELETE r", id=report_id)

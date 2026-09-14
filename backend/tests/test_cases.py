import pytest
from battery_copilot.api import app
from battery_copilot.graph import graph
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


@pytest.fixture
def case_client(monkeypatch):
    def answer(request, case_context=None):
        yield {
            "type": "answer",
            "summary": "已核对给定资料。",
            "claims": [],
            "unknowns": [],
            "next_actions": [],
            "run_id": "test",
            "seconds": 0,
            "usage": {"input_tokens": 0, "output_tokens": 0, "model_calls": 1},
        }

    monkeypatch.setattr("battery_copilot.case_api.run_agent", answer)
    ids = []
    with TestClient(app) as client:
        yield client, ids
        graph().query("MATCH (c:ChangeCase) WHERE c.id IN $ids DELETE c", ids=ids)
    graph.cache_clear()


def create(client, ids, **overrides):
    values = {
        "title": "流程回归",
        "battery_id": 1,
        "target_uid": "kit-v1:fixation:1000",
        "reason": "模拟连接件变更",
        "old_spec": "M6",
        "new_spec": "M8",
        "tool_card": {"id": "TOOL-01", "revision": "B", "supported_specs": ["M6", "M8"]},
        "instruction": {"id": "WI-01", "revision": "B", "spec": "M8"},
        **overrides,
    }
    response = client.post("/api/cases", json=values)
    assert response.status_code == 200, response.text
    case = response.json()
    ids.append(case["id"])
    return case


def analyze(client, case):
    response = client.post(f"/api/cases/{case['id']}/analyze", json={"version": case["version"]})
    assert response.status_code == 200, response.text
    return response.json()


def test_saved_case_requires_current_report_and_review_before_completion(case_client):
    client, ids = case_client
    case = create(client, ids)
    assert client.get(f"/api/cases/{case['id']}").json()["input"]["reason"] == "模拟连接件变更"
    case = analyze(client, case)
    assert case["status"] == "awaiting_review"
    report = case["reports"][-1]
    assert (
        client.post(
            f"/api/cases/{case['id']}/complete", json={"version": case["version"]}
        ).status_code
        == 409
    )
    for finding in report["findings"]:
        case = client.post(
            f"/api/cases/{case['id']}/review",
            json={
                "version": case["version"],
                "report_id": report["id"],
                "finding_id": finding["id"],
                "reviewer": "测试复核人",
                "note": "已核对原始资料。",
            },
        ).json()
    case = client.post(
        f"/api/cases/{case['id']}/complete", json={"version": case["version"]}
    ).json()
    assert case["status"] == "completed"
    export = client.get(f"/api/cases/{case['id']}/export")
    assert export.status_code == 200
    assert "attachment" in export.headers["content-disposition"]
    assert "已完成" in export.text and "测试复核人" in export.text

    old_version = case["version"]
    changed = {**case["input"], "new_spec": "M10"}
    case = client.put(
        f"/api/cases/{case['id']}", json={"version": old_version, "input": changed}
    ).json()
    assert case["status"] == "draft" and case["current_report_id"] is None
    assert case["reports"][0]["reviews"]
    assert (
        client.post(
            f"/api/cases/{case['id']}/complete", json={"version": case["version"]}
        ).status_code
        == 409
    )
    assert (
        client.put(
            f"/api/cases/{case['id']}", json={"version": old_version, "input": changed}
        ).status_code
        == 409
    )
    assert client.get(f"/api/cases/{case['id']}/export").status_code == 409


@pytest.mark.parametrize(
    "tool_card,expected",
    [
        (None, "awaiting_information"),
        ({"id": "TOOL-OLD", "revision": "A", "supported_specs": ["M6"]}, "awaiting_review"),
    ],
)
def test_missing_or_conflicting_card_can_be_supplied_then_reanalyzed(
    case_client, tool_card, expected
):
    client, ids = case_client
    case = analyze(client, create(client, ids, tool_card=tool_card))
    assert case["status"] == expected
    report = case["reports"][-1]
    assert report["findings"][0]["status"] in {"missing", "conflict"}
    assert (
        client.post(
            f"/api/cases/{case['id']}/complete", json={"version": case["version"]}
        ).status_code
        == 409
    )
    assert (
        client.post(
            f"/api/cases/{case['id']}/review",
            json={
                "version": case["version"],
                "report_id": report["id"],
                "finding_id": "tool-fit",
                "reviewer": "测试",
                "note": "不能用确认按钮绕过资料或冲突。",
            },
        ).status_code
        == 409
    )
    case["input"]["tool_card"] = {"id": "TOOL-NEW", "revision": "B", "supported_specs": ["M8"]}
    case = client.put(
        f"/api/cases/{case['id']}", json={"version": case["version"], "input": case["input"]}
    ).json()
    case = analyze(client, case)
    assert case["status"] == "awaiting_review"
    assert len(case["reports"]) == 2
    assert all(f["status"] == "pass" for f in case["reports"][-1]["findings"])
    assert case["reports"][-1]["reviews"] == {}
    assert case["reports"][0]["input"]["tool_card"] == tool_card


def test_analysis_error_keeps_inputs_and_can_retry(case_client, monkeypatch):
    client, ids = case_client
    case = create(client, ids)

    from battery_copilot.case_api import run_agent

    def fail(*args, **kwargs):
        yield {"type": "error", "message": "模拟模型不可用"}

    monkeypatch.setattr("battery_copilot.case_api.run_agent", fail)
    case = analyze(client, case)
    assert case["analysis_status"] == "failed"
    assert case["last_error"] == "模拟模型不可用"
    assert case["status"] == "draft" and case["reports"] == []
    assert client.get(f"/api/cases/{case['id']}").json()["input"]["new_spec"] == "M8"
    monkeypatch.setattr("battery_copilot.case_api.run_agent", run_agent)
    case = analyze(client, case)
    assert case["analysis_status"] == "succeeded" and case["last_error"] is None
    assert len(case["reports"]) == 1


def test_late_analysis_cannot_replace_revised_inputs(case_client):
    from battery_copilot import cases

    client, ids = case_client
    case = create(client, ids)
    started = cases.start_analysis(case["id"], case["version"])
    changed = {**case["input"], "new_spec": "M10"}
    revised = client.put(
        f"/api/cases/{case['id']}", json={"version": started["version"], "input": changed}
    ).json()
    late = cases.finish_analysis(started, {}, [{"type": "error", "message": "过时结果"}])
    assert late == revised
    assert late["input"]["new_spec"] == "M10" and late["last_error"] is None

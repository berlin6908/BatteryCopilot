import json
from types import SimpleNamespace

import pytest
from battery_copilot.agent import AgentRequest, read_evidence, run_agent
from battery_copilot.codex_model import CodexChatModel


def test_summary_supplies_exact_totals_instead_of_requiring_model_arithmetic(monkeypatch):
    rows = [
        {"kind": "Part", "name": "module", "count": 92},
        *[{"kind": "Part", "name": f"singleton-{i}", "count": 1} for i in range(8)],
        {"kind": "Fixation", "name": "screw", "count": 283},
        {"kind": "Operation", "name": "unscrew", "count": 375},
    ]
    monkeypatch.setattr(
        "battery_copilot.agent.graph", lambda: SimpleNamespace(composition=lambda _: rows)
    )
    summary = read_evidence("summary:1", 1)
    assert summary["totals"] == {"Part": 100, "Fixation": 283, "Operation": 375}
    assert json.loads(summary["text"])["totals"] == summary["totals"]


@pytest.mark.parametrize("budget", [None, 2])
def test_agent_reads_missing_citation_after_structured_output_feedback(
    monkeypatch, tmp_path, budget
):
    calls = []
    seen_feedback = []

    def fake_cli(command, **kwargs):
        messages = json.loads(kwargs["input"].split("\n", 1)[1])["messages"]
        results = [m for m in messages if m["type"] == "tool"]
        if not results:
            call = {
                "name": "Answer",
                "args": {
                    "summary": "对象连接关系已确认。",
                    "claims": [
                        {
                            "statement": "连接件连接上盖。",
                            "evidence_ids": ["kit-v1:fixation:1000"],
                            "scope": "record",
                        }
                    ],
                    "unknowns": [],
                    "next_actions": [],
                },
            }
        elif not any(m.get("name") == "read_source" for m in results):
            seen_feedback.append(results[-1]["content"])
            call = {"name": "read_source", "args": {"evidence_id": "kit-v1:fixation:1000"}}
        else:
            call = {
                "name": "Answer",
                "args": {
                    "summary": "对象连接关系已确认。",
                    "claims": [
                        {
                            "statement": "连接件连接上盖。",
                            "evidence_ids": ["kit-v1:fixation:1000"],
                            "scope": "record",
                        }
                    ],
                    "unknowns": [],
                    "next_actions": [],
                },
            }
        calls.append(call["name"])
        events = [
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": json.dumps({"tool_calls": [call]})},
            },
            {"type": "turn.completed", "usage": {"input_tokens": 20, "output_tokens": 5}},
        ]
        return SimpleNamespace(returncode=0, stdout="\n".join(map(json.dumps, events)), stderr="")

    monkeypatch.setattr("battery_copilot.codex_model.subprocess.run", fake_cli)
    monkeypatch.setattr("battery_copilot.agent.model", lambda: CodexChatModel(model_name="test"))
    monkeypatch.setattr("battery_copilot.agent.ROOT", tmp_path)
    monkeypatch.setattr(
        "battery_copilot.agent.read_evidence",
        lambda uid, _: {"uid": uid, "text": "连接件连接上盖。", "source_kind": "record"},
    )
    events = list(
        run_agent(
            AgentRequest(question="连接件1000连接什么？", battery_id=1), max_model_calls=budget
        )
    )
    if budget is not None:
        assert calls == ["Answer", "read_source"]
        assert events[-1]["type"] == "error"
        assert "budget exhausted" in events[-1]["message"]
        assert events[-1]["usage"]["model_calls"] == budget
        return
    assert calls == ["Answer", "read_source", "Answer"]
    assert "kit-v1:fixation:1000" in seen_feedback[0]
    assert events[-1]["type"] == "answer"
    assert events[-1]["usage"]["model_calls"] == 3
    assert any(e["type"] == "validation" for e in events)

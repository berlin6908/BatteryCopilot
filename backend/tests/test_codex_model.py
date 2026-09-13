"""Check the CLI wire protocol through the actual LangGraph tool loop."""

import json
from types import SimpleNamespace

import pytest
from battery_copilot.codex_model import CodexChatModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langchain_core.tools import tool
from pydantic import BaseModel


def test_codex_dispatches_host_tools_and_propagates_failures(monkeypatch):
    executed = []

    @tool
    def read_row(row_id: int) -> dict:
        """Read a source row."""
        executed.append(row_id)
        return {"uid": f"row:{row_id}", "value": 42}

    class Result(BaseModel):
        value: int
        evidence: str

    def fake_cli(command, **kwargs):
        prompt = kwargs["input"]
        transcript = json.loads(prompt.split("\n", 1)[1])["messages"]
        results = [m for m in transcript if m["type"] == "tool"]
        if not results:
            calls = [{"name": "read_row", "args": {"row_id": 7}}]
        else:
            evidence = json.loads(results[-1]["content"])
            calls = [
                {
                    "name": "Result",
                    "args": {"value": evidence["value"], "evidence": evidence["uid"]},
                }
            ]
        events = [
            {
                "type": "item.completed",
                "item": {"type": "agent_message", "text": json.dumps({"tool_calls": calls})},
            },
            {
                "type": "turn.completed",
                "usage": {"input_tokens": 20, "cached_input_tokens": 10, "output_tokens": 5},
            },
        ]
        return SimpleNamespace(returncode=0, stdout="\n".join(map(json.dumps, events)), stderr="")

    monkeypatch.setattr("battery_copilot.codex_model.subprocess.run", fake_cli)
    model = CodexChatModel(model_name="test")
    agent = create_agent(model, [read_row], response_format=ToolStrategy(Result))
    result = agent.invoke({"messages": [{"role": "user", "content": "Read row 7."}]})
    assert executed == [7]
    assert result["structured_response"] == Result(value=42, evidence="row:7")
    assert result["messages"][-2].usage_metadata["input_token_details"]["cache_read"] == 10

    monkeypatch.setattr(
        "battery_copilot.codex_model.subprocess.run",
        lambda *a, **k: SimpleNamespace(
            returncode=1,
            stdout=json.dumps({"type": "turn.failed", "error": {"message": "login required"}}),
            stderr="",
        ),
    )
    with pytest.raises(RuntimeError, match="login required"):
        model.bind_tools([read_row]).invoke("Read row 7.")

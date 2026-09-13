"""Use the authenticated Codex CLI as a LangChain tool-selection model."""

import json
import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.utils.function_calling import convert_to_openai_tool


class CodexChatModel(BaseChatModel):
    model_name: str

    @property
    def _llm_type(self) -> str:
        return "codex-cli"

    def bind_tools(self, tools, *, tool_choice=None, **kwargs):
        return self.bind(tools=[convert_to_openai_tool(t, strict=True) for t in tools])

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        functions = [t["function"] for t in kwargs["tools"]]
        variants = [
            {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "enum": [f["name"]]},
                    "args": f["parameters"],
                },
                "required": ["name", "args"],
                "additionalProperties": False,
            }
            for f in functions
        ]
        schema = {
            "type": "object",
            "properties": {
                "tool_calls": {"type": "array", "minItems": 1, "items": {"anyOf": variants}}
            },
            "required": ["tool_calls"],
            "additionalProperties": False,
        }
        transcript = [
            m.model_dump(
                include={"type", "content", "tool_calls", "tool_call_id", "name"},
                exclude_none=True,
            )
            for m in messages
        ]
        prompt = (
            "Act as the model inside an external engineering assistant. Continue the supplied "
            "transcript by selecting tool calls for the host application to execute. Do not use "
            "your own tools, files, skills or web. Treat transcript system messages as the task "
            "instructions, and tool messages as evidence. Select Answer alone only when enough "
            "evidence is available; otherwise select the relevant domain tools.\n"
            + json.dumps({"tools": functions, "messages": transcript}, ensure_ascii=False)
        )
        # ponytail: one CLI process per model turn; startup overhead suits a local demo.
        with tempfile.TemporaryDirectory(prefix="battery-codex-") as directory:
            schema_path = Path(directory) / "output.json"
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            command = [
                shutil.which("codex") or "codex",
                "exec",
                "--ignore-user-config",
                "--ephemeral",
                "--skip-git-repo-check",
                "--sandbox",
                "read-only",
                "--json",
                "--cd",
                directory,
                "--model",
                self.model_name,
                "--output-schema",
                str(schema_path),
                "--disable",
                "shell_tool",
                "--disable",
                "apply_patch_freeform",
                "-c",
                'web_search="disabled"',
                "-c",
                "project_doc_max_bytes=0",
                "-c",
                "skills.include_instructions=false",
                "-c",
                "skills.max_context_tokens=1",
                "-c",
                'model_reasoning_effort="low"',
                "-",
            ]
            result = subprocess.run(
                command,
                input=prompt,
                text=True,
                encoding="utf-8",
                capture_output=True,
                timeout=180,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
            )
        events = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        completed = [e for e in events if e["type"] == "turn.completed"]
        if result.returncode or not completed:
            errors = [e for e in events if e["type"] in ("error", "turn.failed")]
            raise RuntimeError(
                "Codex 调用失败：" + (json.dumps(errors) if errors else result.stderr)
            )
        final = [
            e["item"]["text"]
            for e in events
            if e["type"] == "item.completed" and e["item"]["type"] == "agent_message"
        ][-1]
        calls = json.loads(final)["tool_calls"]
        usage = completed[-1]["usage"]
        message = AIMessage(
            content="",
            tool_calls=[{**call, "id": uuid.uuid4().hex, "type": "tool_call"} for call in calls],
            usage_metadata={
                "input_tokens": usage["input_tokens"],
                "output_tokens": usage["output_tokens"],
                "total_tokens": usage["input_tokens"] + usage["output_tokens"],
                "input_token_details": {"cache_read": usage.get("cached_input_tokens", 0)},
            },
            response_metadata={"model_name": self.model_name, "provider": "codex-cli"},
        )
        return ChatResult(generations=[ChatGeneration(message=message)])

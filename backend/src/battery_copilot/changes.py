"""Deterministic checks for explicitly simulated engineering changes."""

import json

from battery_copilot.settings import ROOT


def assess_tool_fit(new_spec: str, supported_specs: list[str]) -> dict:
    if not supported_specs:
        return {"status": "unknown", "reason": "工具卡未提供支持规格，需要补充资料。"}
    if new_spec not in supported_specs:
        return {"status": "conflict", "reason": f"新规格 {new_spec} 不在演示工具卡支持范围内。"}
    return {"status": "compatible", "reason": "新规格在演示工具卡支持范围内。"}


def compare_scenario(graph, battery_id: int, scenario_id: str) -> dict:
    scenarios = json.loads((ROOT / "data/scenarios.json").read_text(encoding="utf-8"))
    scenario = next((s for s in scenarios if s["id"] == scenario_id), None)
    if not scenario or scenario["battery_id"] != battery_id:
        raise ValueError("场景不属于当前电池包。")
    local = graph.neighborhood(scenario["target_uid"], battery_id)
    check = assess_tool_fit(scenario["new_spec"], scenario["supported_specs"])
    return {
        **scenario,
        "rule": "TOOL-SPEC-001",
        "check": check,
        "candidates": local["nodes"],
        "paths": local["edges"],
        "evidence_ids": [n["uid"] for n in local["nodes"]] + [scenario["id"]],
        "unknowns": ["真实螺钉规格、扭矩和工具卡未提供。", "候选关联不代表已证明的制造影响。"],
    }

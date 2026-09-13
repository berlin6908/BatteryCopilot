"""Saved change requests, versioned reports and explicit human review."""

import json
import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

from battery_copilot.changes import assess_tool_fit
from battery_copilot.graph import graph

STATUS_LABELS = {
    "draft": "草稿",
    "awaiting_information": "待补充",
    "awaiting_review": "待复核",
    "completed": "已完成",
}


class CaseConflict(Exception):
    pass


class CaseNotFound(Exception):
    pass


class ToolCard(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    id: str = Field(min_length=1, max_length=100)
    revision: str = Field(min_length=1, max_length=40)
    supported_specs: list[str] = Field(max_length=100)


class Instruction(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    id: str = Field(min_length=1, max_length=100)
    revision: str = Field(min_length=1, max_length=40)
    spec: str = Field(min_length=1, max_length=100)


class CaseInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=160)
    battery_id: int = Field(ge=1, le=10)
    target_uid: str = Field(min_length=1, max_length=100)
    reason: str = Field(min_length=1, max_length=2000)
    old_spec: str = Field(min_length=1, max_length=100)
    new_spec: str = Field(min_length=1, max_length=100)
    tool_card: ToolCard | None = None
    instruction: Instruction | None = None


def now():
    return datetime.now(timezone.utc).isoformat()


def list_cases(battery_id: int):
    return graph().query(
        "MATCH (c:ChangeCase {battery_id:$battery_id}) "
        "RETURN c.id AS id,c.title AS title,c.status AS status,c.updated_at AS updated_at "
        "ORDER BY c.updated_at DESC LIMIT 100",
        battery_id=battery_id,
    )


def get_case(case_id: str):
    rows = graph().query("MATCH (c:ChangeCase {id:$id}) RETURN c.payload AS payload", id=case_id)
    if not rows:
        raise CaseNotFound("找不到该变更单。")
    return json.loads(rows[0]["payload"])


def _check_version(case, version):
    if case["version"] != version:
        raise CaseConflict("变更单已更新，请刷新后再操作。")


def _validate_target(values):
    target = graph().record(values.target_uid, values.battery_id)
    if target["kind"] != "Fixation":
        raise ValueError("本轮规格变更请选择当前产品的连接件。")


def _save(case):
    expected = case["version"]
    case["version"] += 1
    case["updated_at"] = now()

    def write(tx):
        # Increment takes Neo4j's write lock; a stale version rolls this transaction back.
        row = tx.run(
            "MATCH (c:ChangeCase {id:$id}) SET c.version=c.version+1 RETURN c.version AS version",
            id=case["id"],
        ).single()
        if row is None or row["version"] != expected + 1:
            raise CaseConflict("变更单已更新，请刷新后再操作。")
        tx.run(
            "MATCH (c:ChangeCase {id:$id}) SET c.payload=$payload,c.title=$title,"
            "c.status=$status,c.updated_at=$updated_at,c.battery_id=$battery_id",
            id=case["id"],
            payload=json.dumps(case, ensure_ascii=False),
            title=case["input"]["title"],
            status=case["status"],
            updated_at=case["updated_at"],
            battery_id=case["input"]["battery_id"],
        ).consume()

    with graph().driver.session(database="neo4j") as session:
        session.execute_write(write)
    return case


def create_case(values: CaseInput):
    _validate_target(values)
    case = {
        "id": "chg-" + uuid.uuid4().hex[:12],
        "version": 1,
        "input_version": 1,
        "input": values.model_dump(),
        "status": "draft",
        "analysis_status": "idle",
        "active_run_id": None,
        "last_error": None,
        "current_report_id": None,
        "reports": [],
        "created_at": now(),
        "updated_at": now(),
    }
    graph().query(
        "CREATE CONSTRAINT change_case_id IF NOT EXISTS FOR (c:ChangeCase) REQUIRE c.id IS UNIQUE"
    )
    graph().query(
        "CREATE (c:ChangeCase {id:$id,version:1,payload:$payload,title:$title,"
        "status:'draft',battery_id:$battery_id,updated_at:$updated_at})",
        id=case["id"],
        payload=json.dumps(case, ensure_ascii=False),
        title=values.title,
        battery_id=values.battery_id,
        updated_at=case["updated_at"],
    )
    return case


def update_case(case_id: str, version: int, values: CaseInput):
    case = get_case(case_id)
    _check_version(case, version)
    _validate_target(values)
    case.update(
        input=values.model_dump(),
        input_version=case["input_version"] + 1,
        status="draft",
        analysis_status="idle",
        active_run_id=None,
        last_error=None,
        current_report_id=None,
    )
    return _save(case)


def start_analysis(case_id: str, version: int):
    case = get_case(case_id)
    _check_version(case, version)
    case.update(
        active_run_id=uuid.uuid4().hex,
        analysis_status="running",
        last_error=None,
        status="draft",
        current_report_id=None,
    )
    return _save(case)


def build_context(case):
    values = case["input"]
    local = graph().neighborhood(values["target_uid"], values["battery_id"])
    prefix = f"change:{case['id']}:v{case['input_version']}"

    def source(suffix, name, contents):
        return {
            "uid": f"{prefix}:{suffix}",
            "name": name,
            "source_kind": "simulation",
            "source_file": f"{case['id']} / 输入版本 {case['input_version']}",
            "text": json.dumps(contents, ensure_ascii=False, indent=2),
        }

    evidence = [source("request", "模拟变更申请", values)]
    findings = []
    card = values["tool_card"]
    card_refs = [evidence[0]["uid"]]
    if card:
        evidence.append(source("tool-card", f"工具卡 {card['id']} · {card['revision']}", card))
        card_refs.append(evidence[-1]["uid"])
    fit = assess_tool_fit(values["new_spec"], card["supported_specs"] if card else [])
    findings.append(
        {
            "id": "tool-fit",
            "title": "工具规格适配",
            "status": {"unknown": "missing", "compatible": "pass", "conflict": "conflict"}[
                fit["status"]
            ],
            "detail": fit["reason"],
            "evidence_ids": card_refs,
            "action": "补充或更新工具卡后重新分析。"
            if fit["status"] != "compatible"
            else "核对工具卡和新规格。",
        }
    )
    instruction = values["instruction"]
    instruction_refs = [evidence[0]["uid"]]
    if instruction:
        evidence.append(
            source(
                "instruction",
                f"作业指导书 {instruction['id']} · {instruction['revision']}",
                instruction,
            )
        )
        instruction_refs.append(evidence[-1]["uid"])
    instruction_status = (
        "missing"
        if not instruction
        else "pass"
        if instruction["spec"] == values["new_spec"]
        else "conflict"
    )
    findings.append(
        {
            "id": "instruction-spec",
            "title": "作业指导书同步",
            "status": instruction_status,
            "detail": "尚未提供作业指导书。"
            if not instruction
            else (
                f"指导书 {instruction['id']}（{instruction['revision']}）"
                f"引用 {instruction['spec']}；"
                f"变更要求 {values['new_spec']}。"
            ),
            "evidence_ids": instruction_refs,
            "action": "补充或更新指导书后重新分析。"
            if instruction_status != "pass"
            else "核对指导书版次和规格。",
        }
    )
    findings.append(
        {
            "id": "related-objects",
            "title": "关联对象清单",
            "status": "pass",
            "detail": (
                f"已找到 {len(local['nodes'])} 个直接关联对象，含变更对象；"
                "请核对连接关系和记录操作。"
            ),
            "action": "核对对象清单；关联不等于已验证的制造影响。",
            "evidence_ids": [node["uid"] for node in local["nodes"]],
        }
    )
    evidence.extend(graph().record(node["uid"], values["battery_id"]) for node in local["nodes"])
    return {
        "case_id": case["id"],
        "input_version": case["input_version"],
        "input": values,
        "findings": findings,
        "related": local["nodes"],
        "paths": local["edges"],
        "evidence": evidence,
        "scope": "真实结构与独立模拟业务资料的复核",
    }


def finish_analysis(started_case, context, events):
    case = get_case(started_case["id"])
    if case["active_run_id"] != started_case["active_run_id"]:
        return case  # The user revised inputs or explicitly started a newer analysis.
    result = events[-1]
    case["active_run_id"] = None
    if result["type"] == "error":
        case.update(analysis_status="failed", last_error=result["message"])
    else:
        report = {
            **context,
            "id": started_case["active_run_id"],
            "number": len(case["reports"]) + 1,
            "created_at": now(),
            "answer": result,
            "reviews": {},
            "trace": [e for e in events if e["type"] in {"tool", "validation"}],
        }
        case["reports"].append(report)
        case.update(
            current_report_id=report["id"],
            analysis_status="succeeded",
            last_error=None,
            status="awaiting_information"
            if any(f["status"] == "missing" for f in report["findings"])
            else "awaiting_review",
        )
    return _save(case)


def current_report(case):
    if not case["current_report_id"] or case["analysis_status"] != "succeeded":
        raise CaseConflict("请先根据当前资料完成分析。")
    return next(r for r in case["reports"] if r["id"] == case["current_report_id"])


def review_finding(case_id, version, report_id, finding_id, reviewer, note):
    case = get_case(case_id)
    _check_version(case, version)
    report = current_report(case)
    if case["status"] == "completed" or report["id"] != report_id:
        raise CaseConflict("只能复核当前未完成的报告。")
    finding = next((f for f in report["findings"] if f["id"] == finding_id), None)
    if not finding or finding["status"] != "pass":
        raise CaseConflict("请先补充资料或解决规则冲突，再重新分析。")
    report["reviews"][finding_id] = {"reviewer": reviewer, "note": note, "at": now()}
    return _save(case)


def complete_case(case_id, version):
    case = get_case(case_id)
    _check_version(case, version)
    report = current_report(case)
    if any(f["status"] != "pass" or f["id"] not in report["reviews"] for f in report["findings"]):
        raise CaseConflict("资料或冲突尚未处理，或仍有未复核条目。")
    case["status"] = "completed"
    report["completed_at"] = now()
    return _save(case)


def export_report(case):
    report = current_report(case)
    values = report["input"]
    lines = [
        f"# {values['title']}",
        "",
        f"变更单：{case['id']}",
        f"状态：{STATUS_LABELS[case['status']]}",
        f"报告：#{report['number']} / {report['id']} · 输入版本 {report['input_version']}",
        f"生成时间：{report['created_at']}",
        "",
        "本报告使用模拟业务资料。",
        "",
        f"变更对象：{values['target_uid']}",
        f"规格：{values['old_spec']} → {values['new_spec']}",
        f"原因：{values['reason']}",
        "",
        "## 复核清单",
        "",
    ]
    for item in report["findings"]:
        lines.extend(
            [
                f"### {item['title']} · {item['status']}",
                "",
                item["detail"],
                item["action"],
                "证据：" + ", ".join(item["evidence_ids"]),
            ]
        )
        review = report["reviews"].get(item["id"])
        lines.append(
            f"复核：{review['reviewer']} · {review['note']} · {review['at']}"
            if review
            else "复核：待处理"
        )
        lines.append("")
    lines.extend(["## Agent 说明", "", report["answer"]["summary"], ""])
    for claim in report["answer"]["claims"]:
        lines.append(f"- {claim['statement']}（{', '.join(claim['evidence_ids'])}）")
    lines.extend(
        [
            "",
            "## 本次输入",
            "",
            "```json",
            json.dumps(values, ensure_ascii=False, indent=2),
            "```",
            "",
            "## 来源",
            "",
        ]
    )
    for evidence in report["evidence"]:
        lines.extend(
            [
                f"### {evidence['uid']}",
                "",
                f"{evidence.get('name', '')} · {evidence['source_file']}",
                evidence["text"],
                "",
            ]
        )
    return "\n".join(lines)

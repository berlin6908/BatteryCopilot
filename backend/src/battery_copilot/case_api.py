"""HTTP actions for the change-request workflow."""

from fastapi import APIRouter, Query
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, Field

from battery_copilot import cases
from battery_copilot.agent import AgentRequest, read_evidence, run_agent
from battery_copilot.graph import graph

router = APIRouter(prefix="/api/cases", tags=["Change requests"])


class Version(BaseModel):
    version: int = Field(ge=1)


class Update(Version):
    input: cases.CaseInput


class Review(Version):
    model_config = ConfigDict(str_strip_whitespace=True)
    report_id: str
    finding_id: str
    reviewer: str = Field(min_length=1, max_length=100)
    note: str = Field(min_length=1, max_length=2000)


@router.get("")
def list_requests(battery_id: int = Query(ge=1, le=10)):
    return cases.list_cases(battery_id)


@router.get("/example")
def example(battery_id: int = Query(ge=1, le=10)):
    target = graph().entities(battery_id, "", "Fixation", 1)[0]
    return cases.CaseInput(
        title="连接件规格变更复核",
        battery_id=battery_id,
        target_uid=target["uid"],
        reason="模拟将连接件规格从 M6 更新为 M8，检查工具和作业指导书。",
        old_spec="M6",
        new_spec="M8",
        tool_card=cases.ToolCard(id="TOOL-01", revision="B", supported_specs=["M6", "M8"]),
        instruction=cases.Instruction(id="WI-01", revision="B", spec="M8"),
    )


@router.post("")
def create(values: cases.CaseInput):
    return cases.create_case(values)


@router.get("/{case_id}")
def detail(case_id: str):
    return cases.get_case(case_id)


@router.put("/{case_id}")
def update(case_id: str, body: Update):
    return cases.update_case(case_id, body.version, body.input)


@router.post("/{case_id}/analyze")
def analyze(case_id: str, body: Version):
    started = cases.start_analysis(case_id, body.version)
    context, events = {}, []
    try:
        context = cases.build_context(started)
        request = AgentRequest(
            battery_id=started["input"]["battery_id"],
            question="复核当前变更单：查看变更资料和关联对象，解释工具适配、作业指导书同步情况。"
            "明确需要补充的具体资料、需要处理的冲突，逐条引用来源。结论限于给定模拟资料。",
        )
        events = list(run_agent(request, case_context=context))
        if not events or events[-1]["type"] not in {"answer", "error"}:
            raise ValueError("分析没有返回完整结果。")
        if events[-1]["type"] == "answer":
            cited = {uid for claim in events[-1]["claims"] for uid in claim["evidence_ids"]}
            saved = {source["uid"] for source in context["evidence"]}
            context["evidence"].extend(
                read_evidence(uid, request.battery_id) for uid in sorted(cited - saved)
            )
    except Exception as exc:
        events.append({"type": "error", "message": str(exc)})
    return cases.finish_analysis(started, context, events)


@router.post("/{case_id}/review")
def review(case_id: str, body: Review):
    return cases.review_finding(case_id, **body.model_dump())


@router.post("/{case_id}/complete")
def complete(case_id: str, body: Version):
    return cases.complete_case(case_id, body.version)


@router.get("/{case_id}/export")
def export(case_id: str):
    case = cases.get_case(case_id)
    return Response(
        cases.export_report(case),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{case["id"]}.md"'},
    )

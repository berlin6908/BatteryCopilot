import json
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel, Field

from battery_copilot import manufacturing as mfg
from battery_copilot.settings import settings

router = APIRouter(prefix="/api/manufacturing", tags=["manufacturing"])


class ReportRequest(BaseModel):
    cell_uid: str
    question: str = Field(min_length=1, max_length=4000)


class Review(BaseModel):
    reviewer: str = Field(min_length=1, max_length=100)
    decision: Literal["verified", "needs_information"]
    note: str = Field(min_length=1, max_length=4000)


@router.get("/cells")
def cells():
    return mfg.catalogue()


@router.get("/trace")
def trace(cell_uid: str):
    return mfg.trace_cell(cell_uid)


@router.get("/process")
def process(cell_uid: str, process_uid: str):
    return mfg.process_details(cell_uid, process_uid)


@router.get("/test")
def test(
    cell_uid: str, test_uid: str, offset: int = Query(0, ge=0), limit: int = Query(12, ge=1, le=40)
):
    return mfg.test_results(cell_uid, test_uid, offset, limit)


@router.get("/source")
def source(cell_uid: str, evidence_uid: str):
    return mfg.read_source(cell_uid, evidence_uid)


@router.post("/reports")
def generate(body: ReportRequest):
    if not settings().model_ready:
        raise HTTPException(503, "请配置并登录模型服务。")
    mfg.require_cell(body.cell_uid)

    def events():
        try:
            for event in mfg.run_report(body.cell_uid, body.question):
                yield json.dumps(event, ensure_ascii=False) + "\n"
        except Exception as exc:
            yield json.dumps({"type": "error", "message": str(exc)}, ensure_ascii=False) + "\n"

    return StreamingResponse(events(), media_type="application/x-ndjson")


@router.get("/reports")
def reports(cell_uid: str):
    return [
        {"id": r["id"], "created_at": r["created_at"], "summary": r["answer"]["summary"]}
        for r in mfg.reports(cell_uid)
    ]


@router.get("/reports/{report_id}")
def report(report_id: str):
    return mfg.get_report(report_id)


@router.post("/reports/{report_id}/review")
def review(report_id: str, body: Review):
    return mfg.review_report(report_id, **body.model_dump())


@router.get("/reports/{report_id}/export")
def export(report_id: str):
    return Response(
        mfg.export_report(mfg.get_report(report_id)),
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{report_id}.md"'},
    )

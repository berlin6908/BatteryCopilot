import json
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from battery_copilot.agent import AgentRequest, read_evidence, run_agent
from battery_copilot.changes import compare_scenario
from battery_copilot.graph import graph
from battery_copilot.retrieval import search
from battery_copilot.settings import DERIVED, PDF, ROOT, settings


@asynccontextmanager
async def lifespan(app):
    yield
    graph().driver.close()


app = FastAPI(title="Battery Engineering Copilot", version="0.1.0", lifespan=lifespan)


@app.exception_handler(ValueError)
async def invalid_request(request, exc):
    return JSONResponse({"detail": str(exc)}, status_code=400)


@app.get("/api/health")
def health():
    graph().driver.verify_connectivity()
    return {
        "status": "ok",
        "model_ready": settings().model_ready,
        "model_name": settings().model_name,
        "model_provider": settings().model_provider,
        "retrieval_ready": (DERIVED / "embedding-report.json").exists(),
    }


@app.get("/api/overview")
def overview():
    return graph().overview()


@app.get("/api/batteries")
def batteries():
    return graph().batteries()


@app.get("/api/entities")
def entities(
    battery_id: int = Query(ge=1, le=10),
    q: str = "",
    kind: Literal["Part", "Fixation", "Operation", "Battery", ""] = "Part",
):
    return graph().entities(battery_id, q, kind)


@app.get("/api/graph/{uid}")
def neighborhood(uid: str, battery_id: int = Query(ge=1, le=10)):
    return graph().neighborhood(uid, battery_id)


@app.get("/api/sequence")
def sequence(
    battery_id: int = Query(ge=1, le=10), offset: int = Query(default=0, ge=0), target_uid: str = ""
):
    return graph().sequence(battery_id, offset, target_uid=target_uid)


@app.get("/api/composition")
def composition(battery_id: int = Query(ge=1, le=10)):
    return graph().composition(battery_id)


@app.get("/api/evidence/{uid}")
def evidence(uid: str, battery_id: int = Query(ge=1, le=10)):
    return read_evidence(uid, battery_id)


@app.get("/api/search")
def search_evidence(
    q: str = Query(min_length=1, max_length=1000),
    battery_id: int = Query(ge=1, le=10),
    scope: Literal["all", "guide"] = "all",
):
    if not (DERIVED / "embedding-report.json").exists():
        raise HTTPException(503, "检索索引尚未建立。")
    return search(q, battery_id, scope)


@app.get("/api/documents/pem/elements")
def document_elements(page: int = Query(default=18, ge=1, le=28)):
    return [
        r["node"]
        for r in graph().query(
            "MATCH (n:Guide {page:$page}) RETURN n{.*,embedding:null} AS node ORDER BY n.uid",
            page=page,
        )
    ]


@app.get("/api/documents/pem/pages/{page}.png")
def page_image(page: int):
    path = DERIVED / "pem" / f"page-{page}.png"
    if not path.is_file():
        raise HTTPException(404, "页面图像尚未解析。")
    return FileResponse(path, media_type="image/png")


@app.get("/api/documents/pem.pdf")
def guide_pdf():
    return FileResponse(PDF, media_type="application/pdf")


@app.get("/api/scenarios")
def scenarios(battery_id: int = Query(ge=1, le=10)):
    return [
        s
        for s in json.loads((ROOT / "data/scenarios.json").read_text(encoding="utf-8"))
        if s["battery_id"] == battery_id
    ]


@app.get("/api/scenarios/{scenario_id}/report")
def scenario_report(scenario_id: str, battery_id: int = Query(ge=1, le=10)):
    return compare_scenario(graph(), battery_id, scenario_id)


@app.post("/api/agent/run")
def agent_run(request: AgentRequest):
    if not settings().model_ready:
        raise HTTPException(
            503, "Agent 等待模型配置：请按 README 连接 Codex 或 API 模型，然后重启后端。"
        )
    return StreamingResponse(
        (json.dumps(event, ensure_ascii=False) + "\n" for event in run_agent(request)),
        media_type="application/x-ndjson",
    )


web_build = ROOT / "frontend/build/web"
if web_build.is_dir():
    app.mount("/", StaticFiles(directory=web_build, html=True), name="workbench")

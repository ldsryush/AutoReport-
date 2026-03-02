from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.models import (
    ExplainReportRequest,
    ExplainReportResponse,
    GenerateSqlDraftRequest,
    GenerateSqlDraftResponse,
    RunReportRequest,
    RunReportResponse,
)
from app.report_catalog import REPORTS
from app.services.database import DatabaseError, DatabaseService
from app.services.mock_data import MockDataError, get_mock_rows
from app.services.openai_helper import OpenAIService, OpenAIServiceError
from app.settings import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent


def _database_service() -> DatabaseService:
    try:
        return DatabaseService(settings.database_url)
    except DatabaseError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


def _openai_service() -> OpenAIService:
    try:
        return OpenAIService(settings.openai_api_key, settings.openai_model)
    except OpenAIServiceError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


@app.get("/")
def ui() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/reports")
def list_reports() -> list[dict[str, str]]:
    return [
        {"report_id": report.report_id, "title": report.title}
        for report in REPORTS.values()
    ]


@app.post("/reports/run", response_model=RunReportResponse)
def run_report(payload: RunReportRequest) -> RunReportResponse:
    report = REPORTS.get(payload.report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Unknown report_id: {payload.report_id}")

    final_params = dict(report.default_params)
    final_params.update(payload.params)

    use_mock_data = (
        payload.use_mock_data if payload.use_mock_data is not None else settings.use_mock_data
    )

    if use_mock_data:
        try:
            rows = get_mock_rows(payload.report_id, final_params)
        except MockDataError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    else:
        db = _database_service()
        try:
            rows = db.run_query(report.sql, final_params)
        except DatabaseError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return RunReportResponse(report_id=payload.report_id, row_count=len(rows), rows=rows)


@app.post("/reports/explain", response_model=ExplainReportResponse)
def explain_report(payload: ExplainReportRequest) -> ExplainReportResponse:
    ai = _openai_service()
    try:
        explanation = ai.explain_report(
            report_id=payload.report_id,
            rows=payload.rows,
            user_goal=payload.user_goal,
        )
    except OpenAIServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ExplainReportResponse(explanation=explanation)


@app.post("/reports/sql-draft", response_model=GenerateSqlDraftResponse)
def generate_sql_draft(payload: GenerateSqlDraftRequest) -> GenerateSqlDraftResponse:
    ai = _openai_service()
    try:
        sql, notes = ai.draft_sql(payload.schema_context, payload.request)
    except OpenAIServiceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return GenerateSqlDraftResponse(sql=sql, notes=notes)

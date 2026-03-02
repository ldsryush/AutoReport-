from typing import Any

from pydantic import BaseModel, Field


class RunReportRequest(BaseModel):
    report_id: str = Field(description="ID of the report from /reports")
    params: dict[str, Any] = Field(default_factory=dict)
    use_mock_data: bool | None = Field(
        default=None,
        description="Override global USE_MOCK_DATA for this request.",
    )


class RunReportResponse(BaseModel):
    report_id: str
    row_count: int
    rows: list[dict[str, Any]]


class ExplainReportRequest(BaseModel):
    report_id: str
    rows: list[dict[str, Any]]
    user_goal: str = Field(default="Explain this report in plain language and give 3 actions.")


class ExplainReportResponse(BaseModel):
    explanation: str


class GenerateSqlDraftRequest(BaseModel):
    schema_context: str = Field(
        description="Tables, columns, and relationships of your existing database."
    )
    request: str = Field(description="What report/query you want to build.")


class GenerateSqlDraftResponse(BaseModel):
    sql: str
    notes: str

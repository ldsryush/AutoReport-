import json

from openai import OpenAI


class OpenAIServiceError(Exception):
    pass


class OpenAIService:
    def __init__(self, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = model

    def explain_report(self, report_id: str, rows: list[dict], user_goal: str) -> str:
        if self.client is None:
            sample = rows[:3]
            return (
                "OpenAI is not configured (missing OPENAI_API_KEY). "
                "This is a local MVP fallback summary.\n\n"
                f"Report: {report_id}\n"
                f"Rows received: {len(rows)}\n"
                f"Goal: {user_goal}\n"
                f"Sample rows: {json.dumps(sample, default=str)}"
            )

        payload = json.dumps(rows[:100], default=str)
        prompt = (
            "You are a senior business analyst. "
            "Explain report output clearly for non-technical users, then provide 3 practical actions.\n\n"
            f"Report ID: {report_id}\n"
            f"User Goal: {user_goal}\n"
            f"Rows (JSON): {payload}"
        )
        try:
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
                temperature=0.2,
            )
            return response.output_text.strip()
        except Exception as exc:
            raise OpenAIServiceError(str(exc)) from exc

    def draft_sql(self, schema_context: str, request: str) -> tuple[str, str]:
        if self.client is None:
            return (
                "SELECT 1 AS placeholder_metric;",
                "OpenAI is not configured, so this is a placeholder SQL draft. "
                "Add OPENAI_API_KEY to enable AI-generated SQL drafts.",
            )

        prompt = (
            "You are an expert SQL engineer. "
            "Return a safe SELECT-only SQL draft and concise notes."
            " If details are missing, state assumptions.\n\n"
            f"Schema context:\n{schema_context}\n\n"
            f"Request:\n{request}\n\n"
            "Return JSON with keys sql and notes."
        )
        try:
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
                temperature=0.1,
            )
            text = response.output_text.strip()
            data = json.loads(text)
            return str(data.get("sql", "")), str(data.get("notes", ""))
        except Exception as exc:
            raise OpenAIServiceError(str(exc)) from exc

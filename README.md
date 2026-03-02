# AutoReport

AutoReport is a FastAPI app that:

- Runs report templates using mock data by default (MVP)
- Can connect to your existing database when enabled
- Uses OpenAI to explain report output in plain language
- Uses OpenAI to draft SQL for new report ideas

## 1) Setup

No virtual environment is required for this MVP.

1. Install dependencies with your system Python:

```bash
py -m pip install -r requirements.txt
```

2. (Optional) Copy `.env.example` to `.env` and fill values:

- `USE_MOCK_DATA=true` for MVP mode
- `DATABASE_URL` only if `USE_MOCK_DATA=false`
- `OPENAI_API_KEY` optional for AI features (fallback responses exist)
- `OPENAI_MODEL`: defaults to `gpt-4.1-mini`

If you skip `.env`, defaults are used (mock data mode is enabled by default).

## 2) Run

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Or use the one-command launcher for collaborators:

```powershell
.\start.ps1

Open Swagger UI:

- http://127.0.0.1:8000/docs

Open the built-in MVP UI:

- http://127.0.0.1:8000/

## 3) Use the app

- `GET /reports` lists available report templates.
- `POST /reports/run` runs a report (mock data by default).
- `POST /reports/explain` sends report rows to OpenAI for explanation.
- `POST /reports/sql-draft` asks OpenAI to draft SELECT-only SQL.

For quick manual testing, use the web UI at `/`.

## 4) MVP behavior

- If `USE_MOCK_DATA=true`, `/reports/run` uses mock rows from `app/services/mock_data.py`.
- To switch to your real DB later, set `USE_MOCK_DATA=false` and provide `DATABASE_URL`.
- If `OPENAI_API_KEY` is missing, AI endpoints return safe fallback text.

## 5) Customize reports

Edit report templates in `app/report_catalog.py`.

> The SQL templates use `orders` and `customers` as examples for real DB mode.

## Example payloads

### Run a report

```json
{
  "report_id": "sales_summary",
  "use_mock_data": true,
  "params": {
    "start_date": "2026-01-01",
    "end_date": "2026-03-01",
    "limit": 50
  }
}
```

### Explain output

```json
{
  "report_id": "sales_summary",
  "rows": [
    {"day": "2026-03-01", "total_orders": 124, "revenue": 15239.55}
  ],
  "user_goal": "Explain trend and suggest next steps"
}
```

### Draft SQL

```json
{
  "schema_context": "orders(id, order_date, customer_id, total_amount), customers(id, name)",
  "request": "Create a monthly retention report by cohort"
}
```

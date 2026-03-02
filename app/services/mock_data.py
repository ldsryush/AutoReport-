from __future__ import annotations

from datetime import date
from typing import Any


class MockDataError(Exception):
    pass


_SALES_SUMMARY_ROWS = [
    {"day": date(2026, 3, 1), "total_orders": 124, "revenue": 15239.55},
    {"day": date(2026, 2, 28), "total_orders": 119, "revenue": 14602.10},
    {"day": date(2026, 2, 27), "total_orders": 108, "revenue": 13011.45},
    {"day": date(2026, 2, 26), "total_orders": 132, "revenue": 16123.00},
    {"day": date(2026, 2, 25), "total_orders": 97, "revenue": 12098.75},
]

_TOP_CUSTOMERS_ROWS = [
    {"customer_id": 101, "customer_name": "Northstar Retail", "total_spend": 84550.10},
    {"customer_id": 204, "customer_name": "Blue Harbor", "total_spend": 78200.40},
    {"customer_id": 309, "customer_name": "Pine Labs", "total_spend": 61120.00},
    {"customer_id": 412, "customer_name": "Sunline Foods", "total_spend": 48890.35},
    {"customer_id": 507, "customer_name": "Moss & Co", "total_spend": 43021.89},
]


def _normalize_limit(value: Any, default: int) -> int:
    try:
        limit = int(value)
        if limit <= 0:
            return default
        return limit
    except (TypeError, ValueError):
        return default


def get_mock_rows(report_id: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    safe_params = params or {}

    if report_id == "sales_summary":
        limit = _normalize_limit(safe_params.get("limit"), 100)
        return _SALES_SUMMARY_ROWS[:limit]

    if report_id == "top_customers":
        limit = _normalize_limit(safe_params.get("limit"), 20)
        return _TOP_CUSTOMERS_ROWS[:limit]

    raise MockDataError(f"No mock data configured for report_id: {report_id}")
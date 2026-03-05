from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class ReportTemplate:
    report_id: str
    title: str
    sql: str
    default_params: Mapping[str, object]


REPORTS: dict[str, ReportTemplate] = {
    "sales_summary": ReportTemplate(
        report_id="sales_summary",
        title="Monthly sales summary",
        sql="""
            SELECT
                DATE_TRUNC('month', order_date)::date AS day,
                COUNT(*) AS total_orders,
                COALESCE(SUM(total_amount), 0) AS revenue
            FROM orders
            WHERE (:start_date IS NULL OR order_date >= :start_date)
              AND (:end_date IS NULL OR order_date <= :end_date)
            GROUP BY DATE_TRUNC('month', order_date)::date
            ORDER BY day DESC
            LIMIT :limit
        """,
        default_params={"start_date": None, "end_date": None, "limit": 100},
    ),
    "top_customers": ReportTemplate(
        report_id="top_customers",
        title="Top customers by spend",
        sql="""
            SELECT
                c.id AS customer_id,
                c.name AS customer_name,
                COALESCE(SUM(o.total_amount), 0) AS total_spend
            FROM customers c
            JOIN orders o ON o.customer_id = c.id
            WHERE (:start_date IS NULL OR o.order_date >= :start_date)
              AND (:end_date IS NULL OR o.order_date <= :end_date)
            GROUP BY c.id, c.name
            ORDER BY total_spend DESC
            LIMIT :limit
        """,
        default_params={"start_date": None, "end_date": None, "limit": 20},
    ),
}

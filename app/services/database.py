from typing import Any

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


class DatabaseError(Exception):
    pass


class DatabaseService:
    def __init__(self, database_url: str) -> None:
        if not database_url:
            raise DatabaseError("DATABASE_URL is missing. Set it in your .env file.")

        self.engine: Engine = create_engine(database_url, pool_pre_ping=True, future=True)

    def run_query(self, sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql), params or {})
                return [dict(row._mapping) for row in result.fetchall()]
        except Exception as exc:
            raise DatabaseError(str(exc)) from exc

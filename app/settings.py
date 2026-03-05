import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env", override=True)


def _clean_env(value: str | None, default: str = "") -> str:
    if value is None:
        return default
    cleaned = value.strip().strip('"').strip("'")
    return cleaned


def _to_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "AutoReport")
    app_env: str = os.getenv("APP_ENV", "development")
    app_host: str = os.getenv("APP_HOST", "127.0.0.1")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    use_mock_data: bool = _to_bool(os.getenv("USE_MOCK_DATA"), True)

    database_url: str = _clean_env(os.getenv("DATABASE_URL"), "")

    openai_api_key: str = _clean_env(os.getenv("OPENAI_API_KEY"), "")
    openai_model: str = _clean_env(os.getenv("OPENAI_MODEL"), "gpt-4.1-mini")


settings = Settings()

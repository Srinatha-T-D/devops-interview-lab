from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_env: str
    database_url: str
    service_version: str


def get_settings() -> Settings:
    return Settings(
        app_env=os.getenv("APP_ENV", "local"),
        database_url=os.getenv(
            "DATABASE_URL", "postgresql://orders:orders@db:5432/orders"
        ),
        service_version=os.getenv("SERVICE_VERSION", "dev"),
    )

import json
import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import Callable

import psycopg
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from app.config import get_settings

REQUESTS = Counter(
    "order_api_http_requests_total", "HTTP requests", ["method", "path", "status"]
)
LATENCY = Histogram(
    "order_api_http_request_duration_seconds",
    "HTTP request duration",
    ["method", "path"],
)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(
            {
                "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
                "level": record.levelname,
                "message": record.getMessage(),
                "request_id": getattr(record, "request_id", None),
                "environment": get_settings().app_env,
            }
        )


logger = logging.getLogger("order-api")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
logger.setLevel(logging.INFO)
logger.propagate = False


def query_database(query: str):
    settings = get_settings()
    with psycopg.connect(settings.database_url, connect_timeout=3) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    logger.info("application_started", extra={"request_id": None})
    logger.info(
        f"configuration_loaded version={settings.service_version}",
        extra={"request_id": None},
    )
    yield
    logger.info("application_stopped", extra={"request_id": None})


app = FastAPI(title="Order API", version="1.0.0", lifespan=lifespan)


@app.middleware("http")
async def observe_request(request: Request, call_next: Callable):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("unhandled_request_error", extra={"request_id": request_id})
        response = JSONResponse(
            status_code=500, content={"detail": "internal server error"}
        )
    elapsed = time.perf_counter() - started
    path = request.url.path
    REQUESTS.labels(request.method, path, response.status_code).inc()
    LATENCY.labels(request.method, path).observe(elapsed)
    response.headers["X-Request-ID"] = request_id
    logger.info(
        f"request_completed method={request.method} path={path} status={response.status_code} duration_ms={elapsed * 1000:.1f}",
        extra={"request_id": request_id},
    )
    return response


@app.get("/livez")
def livez():
    return {"status": "ok", "check": "process"}


@app.get("/readyz")
def readyz():
    try:
        query_database("SELECT 1")
    except Exception as exception:
        logger.warning(
            f"readiness_failed error={type(exception).__name__}",
            extra={"request_id": None},
        )
        return JSONResponse(
            status_code=503, content={"status": "not_ready", "dependency": "postgres"}
        )
    return {"status": "ready", "dependency": "postgres"}


@app.get("/api/v1/orders")
def list_orders():
    rows = query_database("SELECT id, customer, amount, status FROM orders ORDER BY id")
    return {
        "orders": [
            {
                "id": row[0],
                "customer": row[1],
                "amount": float(row[2]),
                "status": row[3],
            }
            for row in rows
        ]
    }


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

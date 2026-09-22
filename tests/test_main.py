import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture()
def client():
    with TestClient(main.app) as test_client:
        yield test_client


def test_liveness_reports_running_process(client: TestClient):
    response = client.get("/livez")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "check": "process"}
    assert response.headers["X-Request-ID"]


def test_request_id_is_preserved_when_supplied_by_caller(client: TestClient):
    response = client.get("/livez", headers={"X-Request-ID": "interview-request-123"})

    assert response.headers["X-Request-ID"] == "interview-request-123"


def test_readiness_reports_ready_when_database_query_succeeds(
    client: TestClient, monkeypatch
):
    monkeypatch.setattr(main, "query_database", lambda _: [(1,)])

    response = client.get("/readyz")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "dependency": "postgres"}


def test_readiness_removes_unhealthy_instance_from_service(
    client: TestClient, monkeypatch
):
    def unavailable_database(_: str):
        raise RuntimeError("simulated database outage")

    monkeypatch.setattr(main, "query_database", unavailable_database)

    response = client.get("/readyz")

    assert response.status_code == 503
    assert response.json() == {"status": "not_ready", "dependency": "postgres"}


def test_orders_returns_database_rows_as_api_contract(client: TestClient, monkeypatch):
    monkeypatch.setattr(
        main,
        "query_database",
        lambda _: [(1, "Acme Retail", 1499.99, "confirmed")],
    )

    response = client.get("/api/v1/orders")

    assert response.status_code == 200
    assert response.json() == {
        "orders": [
            {
                "id": 1,
                "customer": "Acme Retail",
                "amount": 1499.99,
                "status": "confirmed",
            }
        ]
    }


def test_orders_returns_generic_error_when_database_is_unavailable(
    client: TestClient, monkeypatch
):
    def unavailable_database(_: str):
        raise RuntimeError("simulated database outage")

    monkeypatch.setattr(main, "query_database", unavailable_database)

    response = client.get("/api/v1/orders")

    assert response.status_code == 500
    assert response.json() == {"detail": "internal server error"}
    assert response.headers["X-Request-ID"]

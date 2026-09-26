from fastapi.testclient import TestClient

from crisol import __version__


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app": "El Crisol",
        "version": __version__,
        "environment": "test",
    }


def test_responses_carry_request_id(client: TestClient) -> None:
    response = client.get("/health", headers={"x-request-id": "abc123"})

    assert response.headers["x-request-id"] == "abc123"

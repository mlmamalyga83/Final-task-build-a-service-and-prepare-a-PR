from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api.routes import init_routes
from main import app
from services.summarizer import Summarizer


@pytest.fixture
def client():
    s = Summarizer()
    init_routes(s)
    with TestClient(app) as c:
        yield c


def test_process_success(client):
    with patch("services.summarizer.call_llm", return_value="Краткий пересказ."):
        resp = client.post("/process", json={"text": "Длинный текст для проверки."})
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary"] == "Краткий пересказ."
        assert "model" in data
        assert "cached" in data


def test_process_empty_text(client):
    resp = client.post("/process", json={"text": ""})
    assert resp.status_code == 422


def test_process_long_text(client):
    long_text = "a" * 10001
    resp = client.post("/process", json={"text": long_text})
    assert resp.status_code == 422


def test_process_missing_field(client):
    resp = client.post("/process", json={})
    assert resp.status_code == 422

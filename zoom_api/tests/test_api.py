import os
import sys
import pytest
from fastapi.testclient import TestClient
from datetime import datetime

# Add app to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.config import get_settings

client = TestClient(app)
settings = get_settings()

API_KEY = "test_key_123"
HEADERS = {"X-API-Key": API_KEY}

# Override settings for testing if needed, but we are using .env which has test values

def test_health():
    response = client.get("/api/health", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_auth_failure():
    response = client.get("/api/clases")
    assert response.status_code == 403

def test_get_clases():
    response = client.get("/api/clases", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert data["meta"]["total"] > 0

def test_get_clases_filter():
    # Filter by month '11' (November)
    response = client.get("/api/clases?mes=11", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) > 0
    # Verify all results are from month 11
    for item in data["data"]:
        start_time = datetime.fromisoformat(item["Start Time"])
        assert start_time.month == 11

def test_get_estadisticas():
    response = client.get("/api/estadisticas", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    assert "total_clases" in data
    assert "promedio_duracion_minutos" in data

def test_get_profesores():
    response = client.get("/api/profesores", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) > 0

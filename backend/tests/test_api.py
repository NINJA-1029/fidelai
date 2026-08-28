from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_financial_state_endpoint():
    response = client.get("/api/v1/financial-state?user_id=user_demo_01")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user_demo_01"
    assert "current_balance" in data
    assert "projected_balance" in data


def test_dashboard_endpoint():
    response = client.get("/api/v1/dashboard?user_id=user_demo_01")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user_demo_01"
    assert "financial_state" in data
    assert "active_risks" in data


def test_simulation_endpoint():
    payload = {
        "user_id": "user_demo_01",
        "scenario_type": "unexpected_expense",
        "amount": 12000.0,
        "description": "Urgent Medical Care"
    }
    response = client.post("/api/v1/simulation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user_demo_01"
    assert data["scenario_type"] == "unexpected_expense"
    assert "simulated_projected_balance" in data

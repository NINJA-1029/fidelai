from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "system" in data


def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_ingest_transaction_valid():
    payload = {
        "transaction_id": "txn_test_001",
        "user_id": "user_demo_01",
        "account_id": "acc_checking_01",
        "amount": 2500.0,
        "currency": "INR",
        "type": "debit",
        "category": "groceries",
        "description": "Supermarket Purchase",
        "timestamp": "2026-08-28T12:00:00Z",
        "source": "manual",
        "confidence": 1.0,
        "is_recurring": False
    }
    response = client.post("/api/v1/transactions", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_id"] == "txn_test_001"
    assert data["amount"] == 2500.0


def test_ingest_transaction_invalid_validation_error():
    # Missing required fields like user_id and amount
    payload = {
        "transaction_id": "txn_test_bad",
        "description": "Incomplete transaction"
    }
    response = client.post("/api/v1/transactions", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    assert "message" in data
    assert "details" in data
    assert "timestamp" in data


def test_ingest_financial_event_valid():
    payload = {
        "event_id": "evt_test_001",
        "user_id": "user_demo_01",
        "event_type": "income_received",
        "timestamp": "2026-08-28T12:00:00Z",
        "source": "bank_feed",
        "confidence": 1.0,
        "payload": {"amount": 75000.0, "source": "Tech Corp Salary"}
    }
    response = client.post("/api/v1/financial-events", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["event_id"] == "evt_test_001"
    assert data["event_type"] == "income_received"


def test_financial_state_endpoint():
    response = client.get("/api/v1/financial-state?user_id=user_demo_01")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user_demo_01"
    assert "current_balance" in data
    assert "projected_balance" in data
    assert "risk_signals" in data
    assert "opportunity_signals" in data


def test_dashboard_endpoint():
    response = client.get("/api/v1/dashboard?user_id=user_demo_01")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user_demo_01"
    assert "financial_state" in data
    assert "active_risks" in data
    assert "forecast_30_days" in data


def test_agent_analyze_endpoint():
    payload = {
        "user_id": "user_demo_01",
        "user_query": "Can I afford a new laptop worth 45000 INR?"
    }
    response = client.post("/api/v1/agent/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user_demo_01"
    assert "recommendation" in data
    assert "reason" in data
    assert "evidence" in data


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
    assert "buffer_violation_risk" in data


def test_recommendations_endpoint():
    response = client.get("/api/v1/recommendations?user_id=user_demo_01")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["user_id"] == "user_demo_01"


def test_http_404_error_handler():
    response = client.get("/api/v1/non_existent_route")
    assert response.status_code == 404
    data = response.json()
    assert data["error_code"] == "HTTP_404"
    assert "message" in data

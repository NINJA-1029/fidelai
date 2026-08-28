from fastapi.testclient import TestClient
from backend.main import app
from backend.api.auth import SupabaseAuthService

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


def test_auth_me_and_dev_token_generation():
    # 1. Generate dev token
    token_resp = client.post("/api/v1/auth/token?user_id=user_demo_01&email=test@fidel.finance")
    assert token_resp.status_code == 200
    token_data = token_resp.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # 2. Query /auth/me with Bearer token
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = client.get("/api/v1/auth/me", headers=headers)
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["user_id"] == "user_demo_01"
    assert me_data["email"] == "test@fidel.finance"
    assert me_data["is_authenticated"] is True


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


def test_agent_analyze_and_memory_history_endpoint():
    payload = {
        "user_id": "user_demo_01",
        "user_query": "Can I afford a new laptop worth 45000 INR?"
    }
    # 1. Run analysis
    analyze_resp = client.post("/api/v1/agent/analyze", json=payload)
    assert analyze_resp.status_code == 200
    analyze_data = analyze_resp.json()
    assert analyze_data["user_id"] == "user_demo_01"
    assert "recommendation" in analyze_data

    # 2. Query Long-Term Memory history
    history_resp = client.get("/api/v1/agent/history?user_id=user_demo_01")
    assert history_resp.status_code == 200
    history_data = history_resp.json()
    assert isinstance(history_data, list)
    assert len(history_data) >= 1
    assert history_data[0]["user_id"] == "user_demo_01"


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

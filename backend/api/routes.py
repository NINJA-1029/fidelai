from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from shared.contracts.contracts import (
    Transaction,
    FinancialEvent,
    FinancialState,
    AgentRequest,
    AgentResponse,
    DashboardResponse,
    SimulationRequest,
    SimulationResult,
)
from backend.services.orchestrator import orchestrator
from backend.repositories.financial_repository import repo
from backend.api.auth import get_current_user, AuthenticatedUser, SupabaseAuthService

router = APIRouter(prefix="/api/v1")


# --- System & Authentication Routes ---

@router.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "service": "Agentic Financial Management Backend"}


@router.get("/auth/me", response_model=AuthenticatedUser, tags=["Authentication"])
def get_auth_profile(current_user: AuthenticatedUser = Depends(get_current_user)):
    """
    Returns the currently authenticated Supabase / development user profile.
    """
    return current_user


@router.post("/auth/token", tags=["Authentication"])
def generate_dev_token(user_id: str = "user_demo_01", email: str = "demo@fidel.finance"):
    """
    Generates a development JWT token for local testing and emulator authentication.
    """
    token = SupabaseAuthService.create_development_token(user_id=user_id, email=email)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user_id,
        "email": email,
    }


# --- Ingestion Routes ---

@router.get("/transactions", response_model=List[Transaction], tags=["Ingestion"])
def get_transactions(
    user_id: Optional[str] = Query(None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    target_user = user_id or current_user.user_id
    return repo.get_transactions(target_user)


@router.post("/transactions", response_model=Transaction, tags=["Ingestion"])
def ingest_transaction(
    transaction: Transaction,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        orchestrator.process_transaction(transaction)
        return transaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/financial-events", response_model=FinancialEvent, tags=["Ingestion"])
def ingest_financial_event(
    event: FinancialEvent,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        orchestrator.process_incoming_event(event)
        return event
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- Analytics & Financial State ---

@router.get("/financial-state", response_model=FinancialState, tags=["Financial State"])
def get_financial_state(
    user_id: Optional[str] = Query(None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    target_user = user_id or current_user.user_id
    try:
        return orchestrator.get_current_financial_state(target_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard", response_model=DashboardResponse, tags=["Dashboard"])
def get_dashboard_data(
    user_id: Optional[str] = Query(None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    target_user = user_id or current_user.user_id
    try:
        return orchestrator.get_dashboard(target_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- AI Advisor & Long-Term Memory ---

@router.post("/agent/analyze", response_model=AgentResponse, tags=["AI Advisor"])
def analyze_finances(
    request: AgentRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        state = orchestrator.get_current_financial_state(request.user_id)
        return orchestrator.agent.run(request, state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/query", response_model=AgentResponse, tags=["AI Advisor"])
def query_agent(
    request: AgentRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        state = orchestrator.get_current_financial_state(request.user_id)
        return orchestrator.agent.run(request, state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent/history", response_model=List[AgentResponse], tags=["AI Advisor"])
def get_agent_memory_history(
    user_id: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Retrieves historical agent decision memories and previous recommendation records.
    """
    target_user = user_id or current_user.user_id
    return repo.get_agent_memories(target_user, limit=limit)


@router.get("/recommendations", response_model=List[AgentResponse], tags=["AI Advisor"])
def get_recommendations(
    user_id: Optional[str] = Query(None),
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    target_user = user_id or current_user.user_id
    try:
        state = orchestrator.get_current_financial_state(target_user)
        req = AgentRequest(user_id=target_user)
        advice = orchestrator.agent.run(req, state)
        return [advice]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- What-If Simulation Routes ---

@router.post("/simulation", response_model=SimulationResult, tags=["Simulations"])
def run_simulation(
    request: SimulationRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        return orchestrator.run_simulation(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/simulate", response_model=SimulationResult, tags=["Simulations"])
def simulate_scenario(
    request: SimulationRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    try:
        return orchestrator.run_simulation(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

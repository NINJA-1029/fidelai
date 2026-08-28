from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
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

router = APIRouter(prefix="/api/v1")


@router.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "service": "Agentic Financial Management Backend"}


@router.post("/transactions", response_model=Transaction, tags=["Ingestion"])
def ingest_transaction(transaction: Transaction):
    try:
        orchestrator.process_transaction(transaction)
        return transaction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/financial-events", response_model=FinancialEvent, tags=["Ingestion"])
def ingest_financial_event(event: FinancialEvent):
    try:
        orchestrator.process_incoming_event(event)
        return event
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/financial-state", response_model=FinancialState, tags=["Financial State"])
def get_financial_state(user_id: str = Query("user_demo_01")):
    try:
        return orchestrator.get_current_financial_state(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agent/analyze", response_model=AgentResponse, tags=["AI Advisor"])
def analyze_finances(request: AgentRequest):
    try:
        state = orchestrator.get_current_financial_state(request.user_id)
        return orchestrator.agent.run(request, state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/simulation", response_model=SimulationResult, tags=["Simulations"])
def run_simulation(request: SimulationRequest):
    try:
        return orchestrator.run_simulation(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/dashboard", response_model=DashboardResponse, tags=["Dashboard"])
def get_dashboard_data(user_id: str = Query("user_demo_01")):
    try:
        return orchestrator.get_dashboard(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations", response_model=List[AgentResponse], tags=["AI Advisor"])
def get_recommendations(user_id: str = Query("user_demo_01")):
    try:
        state = orchestrator.get_current_financial_state(user_id)
        req = AgentRequest(user_id=user_id)
        advice = orchestrator.agent.run(req, state)
        return [advice]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

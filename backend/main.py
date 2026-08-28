import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from shared.contracts.contracts import APIError
from backend.api.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("fidel.backend")

app = FastAPI(
    title="Agentic AI Financial Management System",
    version="1.0.0",
    description="Deterministic Financial Analytics and Explainable Local AI Reasoning API"
)

# CORS middleware for local Flutter development and remote clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    error_payload = APIError(
        error_code="INTERNAL_SERVER_ERROR",
        message=str(exc) or "An unexpected internal error occurred."
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_payload.model_dump(mode="json")
    )


# Include API routes
app.include_router(router)


@app.get("/")
def root():
    return {
        "system": "Agentic AI Financial Management System",
        "status": "operational",
        "docs_url": "/docs",
        "health_check": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

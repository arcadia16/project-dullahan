from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import APP_MODE, AGENT_API_KEY
from routers.shared import set_api_keys
from routers.agent import router as agent_router
from routers.orchestrator import router as orch_router

# Set global API keys for dependency injection
set_api_keys(agent_key=AGENT_API_KEY)

app = FastAPI(title="NTLM Audit Tool")


# Health endpoint (common to both modes)
@app.get("/health")
async def health():
    return {"status": "alive"}


# Mode-specific setup
if APP_MODE == "agent":
    # Agent mode: no CORS (server-to-server only)
    app.include_router(agent_router)
    print("Running in AGENT mode on port 8001")
else:
    # Orchestrator mode: add CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",  # Vite dev server
            "http://localhost:3000",  # Alternative dev port
            "http://localhost:8000",  # Orchestrator itself (if frontend served from same origin)
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],  # Restrict methods
        allow_headers=["Content-Type", "Authorization"],
    )
    app.include_router(orch_router)
    print("Running in ORCHESTRATOR mode on port 8000")

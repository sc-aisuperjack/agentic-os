import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from contextlib import asynccontextmanager

# 2025 standards: Absolute imports for Python 3.14
from app.loader import initialize_agents
from app.graph import AgenticOSGraph

# Setup high-visibility logging
logger = logging.getLogger("orchestrator")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# --- 1. Global Engine State ---
# Keeping these globals allows the graph logic to stay in memory
AGENT_REGISTRY = {}
ORCHESTRATOR_ENGINE = None

class OrchestrationRequest(BaseModel):
    task: str
    user_id: str
    preferred_agent: Optional[str] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan management for the AI Superjack Brain.
    Pre-loads agents and compiles the LangGraph once.
    """
    global AGENT_REGISTRY, ORCHESTRATOR_ENGINE
    
    logger.info("🧠 AI SUPERJACK: Brain Initializing...")
    
    # 1. Discovery phase
    AGENT_REGISTRY = initialize_agents()
    
    if not AGENT_REGISTRY:
        logger.error("🚨 CRITICAL: No agents found! Mesh will be non-functional.")
    else:
        # 2. Build the graph engine once during startup
        logger.info(f"🧬 Building Graph with agents: {list(AGENT_REGISTRY.keys())}")
        ORCHESTRATOR_ENGINE = AgenticOSGraph(AGENT_REGISTRY)
        logger.info("✅ AI SUPERJACK: Brain fully operational.")
    
    yield
    # Shutdown logic goes here
    logger.info("💤 Brain entering sleep mode...")

# --- 2. FastAPI Setup ---
app = FastAPI(
    title="AI Superjack Agentic OS Orchestrator",
    version="2.0.25",
    lifespan=lifespan
)

@app.get("/health")
async def health():
    """Mesh health check with agent inventory."""
    return {
        "status": "online",
        "brain": "active" if ORCHESTRATOR_ENGINE else "initializing",
        "agents_loaded": list(AGENT_REGISTRY.keys()),
        "version": "2.0.25"
    }

# --- 3. The Orchestration Logic ---
@app.post("/chat")
async def orchestrate(request: OrchestrationRequest):
    """
    The main thinking loop. Triggered by the Gateway.
    """
    logger.info(f"⚡ Mission Received | User: {request.user_id} | Task: {request.task[:50]}...")
    
    if not ORCHESTRATOR_ENGINE:
        logger.error("❌ Orchestration attempt on uninitialized engine.")
        raise HTTPException(
            status_code=503, 
            detail="Brain engine is currently offline or loading agents."
        )

    try:
        # 4. Invoke the LangGraph workflow
        # We call the .run() method we just fixed in graph.py
        final_state = await ORCHESTRATOR_ENGINE.run(
            task=request.task,
            user_id=request.user_id
        )

        logger.info(f"✅ Mission Success for {request.user_id}")

        # 5. Return the full structured payload
        return {
            "status": "success",
            "final_output": final_state.get("final_output"),
            "agent_chain": final_state.get("history", []),
            "metadata": {
                "version": "2.0.25",
                "engine": "AI-Superjack-v2",
                "timestamp": "2025-12-29"
            }
        }

    except Exception as e:
        logger.error(f"🚨 BRAIN FAILURE: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Orchestration Error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    # Listening on 8001 inside the container
    uvicorn.run(app, host="0.0.0.0", port=8001)
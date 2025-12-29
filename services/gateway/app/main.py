import os
import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx
# Importing shared logic (Assuming installed as local package or path added)
# from shared.models.state import AgentRequest, AgentResponse
# from shared.utils.logger import setup_structured_logging

app = FastAPI(
    title="AI Superjack Agentic OS Gateway",
    version="2.0.25",
    description="Secure entry point for the Dynamic Agentic Mesh"
)

# 1. Standard 2025 Security: CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tighten this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Structured Logging setup
logger = logging.getLogger("gateway")

# --- Simplified Pydantic Models (Usually in shared/models/state.py) ---
class UserQuery(BaseModel):
    task: str
    user_id: str
    preferred_agent: Optional[str] = None # e.g., "researcher"
    model_override: Optional[str] = None  # e.g., "gpt-5"

@app.on_event("startup")
async def startup_event():
    """
    Called on service start. This is where we confirm 
    Environment (Render vs Local) through our loader.
    """
    # Note: In a real mesh, we'd call initialize_engine() from loader here
    env_status = "RENDER" if os.getenv("RENDER") else "LOCAL"
    logger.info(f"🚀 Gateway booting in {env_status} mode...")

@app.get("/health")
async def health_check():
    return {"status": "online", "mesh": "active", "version": "2.0.25"}

@app.post("/chat")
async def process_task(query: UserQuery):
    logger.info(f"📥 Gateway routing task: {query.task[:50]}...")
    
    # Internal Docker address for the Orchestrator
    ORCHESTRATOR_URL = "http://orchestrator:8001/chat" 

    try:
        async with httpx.AsyncClient() as client:
            # CEO MOVE: Hand the baton to the Orchestrator
            response = await client.post(
                ORCHESTRATOR_URL, 
                json=query.dict(),
                timeout=120.0 # High timeout for GPT-5.2 reasoning
            )
            
            if response.status_code != 200:
                logger.error(f"🚨 Orchestrator failed: {response.text}")
                raise HTTPException(status_code=response.status_code, detail="Orchestrator error")
            
            return response.json() # Return the REAL ROI roadmap to the user
            
    except Exception as e:
        logger.error(f"❌ Mesh routing failed: {str(e)}")
        return {"status": "error", "message": "The brain is offline."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
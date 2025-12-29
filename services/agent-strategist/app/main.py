import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from .analysis import StrategicEngine

# Standard 2025 Structured Logging
logger = logging.getLogger("agent-strategist")

app = FastAPI(title="AI Superjack Strategist Worker", version="2025.12")
engine = StrategicEngine()

class StrategyRequest(BaseModel):
    research_data: List[Dict[str, Any]]
    original_task: str

@app.get("/health")
async def health():
    return {"status": "active", "service": "agent-strategist", "runtime": "Python 3.14"}

@app.post("/analyze")
async def analyze_and_plan(request: StrategyRequest):
    """
    Takes research results and builds a high-level strategy 
    using GPT-5.2 Reasoning Effort.
    """
    try:
        logger.info(f"🧠 Analyzing research for task: {request.original_task[:50]}...")
        strategy = await engine.generate_plan(request.original_task, request.research_data)
        return {"strategy": strategy}
    except Exception as e:
        logger.error(f"❌ Strategy Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Strategic engine failure.")
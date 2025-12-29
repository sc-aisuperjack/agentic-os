import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .search import VectorSearchEngine

app = FastAPI(title="AI Superjack Research Worker", version="2025.12")

# Initialize the Search Engine on startup
search_engine = VectorSearchEngine()

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

@app.get("/health")
async def health():
    return {"status": "active", "service": "agent-research", "runtime": "Python 3.14"}

@app.post("/search")
async def perform_search(request: SearchRequest):
    """
    Accepts a query, embeds it, and returns the most relevant 
    chunks from MongoDB Atlas.
    """
    try:
        results = await search_engine.find_relevant_context(request.query, request.limit)
        return {"results": results}
    except Exception as e:
        print(f"❌ Research Search Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Search engine failure.")
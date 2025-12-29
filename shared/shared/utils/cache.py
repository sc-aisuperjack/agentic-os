import os
from motor.motor_asyncio import AsyncIOMotorClient
from langchain_openai import OpenAIEmbeddings
from datetime import datetime, timezone

class SemanticCache:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("MONGO_DB_NAME", "agentic_os")]
        self.collection = self.db["semantic_cache"]
        
        # 2025 Standard: text-embedding-3-small (Fast & Cheap)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.threshold = 0.95

    async def get(self, query: str) -> str | None:
        """Checks if a semantically similar query exists."""
        vector = await self.embeddings.aembed_query(query)
        
        # MongoDB Atlas Vector Search Pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "cache_vector_index",
                    "path": "query_embedding",
                    "queryVector": vector,
                    "numCandidates": 10,
                    "limit": 1
                }
            },
            {"$project": {"answer": 1, "score": {"$meta": "vectorSearchScore"}}}
        ]
        
        async for doc in self.collection.aggregate(pipeline):
            if doc["score"] >= self.threshold:
                return doc["answer"]
        return None

    async def set(self, query: str, answer: str):
        """Stores a new query-answer pair with its embedding."""
        vector = await self.embeddings.aembed_query(query)
        await self.collection.insert_one({
            "query": query,
            "answer": answer,
            "query_embedding": vector,
            "created_at": datetime.now(timezone.utc)
        })
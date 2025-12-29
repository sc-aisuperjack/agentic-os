import os
from pymongo import AsyncMongoClient
from langchain_openai import OpenAIEmbeddings # Or GoogleGenAIEmbeddings

class VectorSearchEngine:
    def __init__(self):
        # 1. Setup Mongo Connection
        self.uri = os.getenv("MONGO_URI")
        self.client = AsyncMongoClient(self.uri)
        self.db = self.client[os.getenv("MONGO_DB_NAME", "agentic_os")]
        self.collection = self.db["knowledge_base"]
        
        # 2. Setup Embeddings Model (Using OpenAI as the RAG gold standard)
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", 
            api_key=os.getenv("OPENAI_API_KEY")
        )

    async def find_relevant_context(self, query: str, limit: int):
        # Generate embedding for the incoming query
        query_vector = await self.embeddings.aembed_query(query)

        # MongoDB 2025 Vector Search Pipeline
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_vector,
                    "numCandidates": limit * 10, # ANN recall tuning
                    "limit": limit
                }
            },
            {
                "$project": {
                    "text": 1,
                    "metadata": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        cursor = self.collection.aggregate(pipeline)
        results = []
        async for doc in cursor:
            results.append({
                "content": doc["text"],
                "source": doc.get("metadata", {}).get("source", "unknown"),
                "score": doc["score"]
            })
        return results
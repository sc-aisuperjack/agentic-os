/**
 * AI SUPERJACK - Agentic OS Vector Initialization
 * Setup for RAG and Semantic Caching (2025 Standard)
 */

// 1. Initialize the Replica Set (Required for Vector Search locally)
try {
  rs.initiate();
  print("✅ Replica Set Initialized");
} catch (e) {
  print("ℹ️ Replica Set already initialized or skipping...");
}

const dbName = "agentic_os";
const db = db.getSiblingDB(dbName);

// 2. Create the RAG Knowledge Collection & Vector Index
db.createCollection("knowledge_base");
db.knowledge_base.createSearchIndex("vector_index", "vectorSearch", {
  fields: [
    {
      type: "vector",
      path: "embedding",
      numDimensions: 1536, // Standard for OpenAI text-embedding-3-small/large
      similarity: "cosine",
    },
    {
      type: "filter",
      path: "metadata.source",
    },
  ],
});
print("🧠 RAG Vector Index created on 'knowledge_base'");

// 3. Create the Semantic Cache Collection & Vector Index
db.createCollection("semantic_cache");
db.semantic_cache.createSearchIndex("cache_vector_index", "vectorSearch", {
  fields: [
    {
      type: "vector",
      path: "query_embedding",
      numDimensions: 1536,
      similarity: "cosine",
    },
  ],
});

// Also add a TTL index for the cache (e.g., expire after 30 days)
db.semantic_cache.createIndex(
  { created_at: 1 },
  { expireAfterSeconds: 2592000 }
);
print("⚡ Semantic Cache Vector Index created on 'semantic_cache'");

print("🚀 Mongo-Init Sequence Complete. AI Superjack Mesh is ready for data.");

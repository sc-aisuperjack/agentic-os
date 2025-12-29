import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

class LLMFactory:
    @staticmethod
    def create(config: dict):
        model_name = config.get("model", "gpt-4o") # Fallback
        
        # --- Gemini 3 Pro (2025 Dynamic Thinking) ---
        if "gemini-3" in model_name:
            return ChatGoogleGenerativeAI(
                model=model_name,
                # High level maximizes reasoning depth for researchers
                thinking_level=config.get("reasoning_effort", "high"),
                google_api_key=os.getenv("GEMINI_API_KEY")
            )
        
        # --- GPT-5.2 (2025 Reasoning Effort) ---
        if "gpt-5" in model_name:
            return ChatOpenAI(
                model=model_name,
                reasoning_effort=config.get("reasoning_effort", "medium"), # Pass directly
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )

        return ChatOpenAI(model="gpt-4o")
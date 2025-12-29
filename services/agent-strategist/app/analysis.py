import os
from langchain_openai import ChatOpenAI

class StrategicEngine:
    def __init__(self):
        # Initializing GPT-5.2 with specific 2025 parameters
        self.model = ChatOpenAI(
            model="gpt-5",
            api_key=os.getenv("OPENAI_API_KEY"),
            # Pro settings for strategy: high reasoning, low verbosity
            model_kwargs={
                "reasoning_effort": "high",
                "text": {"verbosity": "low"} 
            }
        )

    async def generate_plan(self, task: str, data: list):
        # Format the research data into a readable block
        context_block = "\n".join([f"- {d['content']}" for d in data])
        
        prompt = f"""
        YOU ARE THE CHIEF STRATEGIST FOR AI SUPERJACK.
        
        TASK: {task}
        RAW RESEARCH DATA:
        {context_block}
        
        OBJECTIVE:
        Synthesize this data into a 3-point actionable strategy. 
        Focus on ROI, scalability, and marketing impact.
        Keep it 'low verbosity'—direct and punchy.
        """
        
        response = await self.model.ainvoke(prompt)
        return response.content
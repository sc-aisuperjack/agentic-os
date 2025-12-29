from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Annotated
import operator
from .factory import LLMFactory

# --- 1. Define the AI Superjack State Model ---
class GraphState(TypedDict):
    task: str
    # Annotated with operator.add allows history to grow as agents append to it
    history: Annotated[List[str], operator.add] 
    next_agent: str
    final_output: str
    user_id: str

class AgenticOSGraph:
    def __init__(self, agents: dict):
        self.agents = agents
        self.builder = StateGraph(GraphState)
        self._build_workflow()

    def _build_workflow(self):
        # 1. Routing Node: Decides which agent to call
        self.builder.add_node("router", self.route_task)
        
        # 2. Dynamic Agent Nodes: Created on the fly from the registry
        for agent_id in self.agents:
            self.builder.add_node(agent_id, self.execute_agent)

        self.builder.set_entry_point("router")
        
        # Conditional Edges based on the 'next_agent' state
        # This maps the router's decision to the actual node name
        self.builder.add_conditional_edges(
            "router",
            lambda x: x["next_agent"],
            {aid: aid for aid in self.agents}
        )
        
        # After any agent finishes, they head to the finish line (END)
        for agent_id in self.agents:
            self.builder.add_edge(agent_id, END)

        # 3. Compile the Graph into an executable binary
        self.graph = self.builder.compile()

    # --- NODE LOGIC ---

    async def route_task(self, state: GraphState):
        """Decides which agent is best for the job based on capability mapping."""
        task_text = state["task"].lower()
        
        selected_agent = "strategist"  # Default fallback
        
        for aid, data in self.agents.items():
            capability = data['config'].get('capability', '').lower()
            if capability and capability in task_text:
                selected_agent = aid
                break
        
        return {
            "next_agent": selected_agent,
            "history": [f"Router selected: {selected_agent}"]
        }

    async def execute_agent(self, state: GraphState):
        """The heavy lifting. Calls the specific LLM via the Factory."""
        agent_id = state["next_agent"]
        config = self.agents[agent_id]
        
        # Create the LLM instance (Gemini/GPT-5.2) on the fly
        llm = LLMFactory.create(config['config'])
        
        # Assemble the full prompt from the Markdown instructions
        full_prompt = f"{config['prompt']}\n\nTask: {state['task']}"
        
        # Execute the AI call
        response = await llm.ainvoke(full_prompt)
        
        return {
            "final_output": response.content,
            "history": [f"Executed: {agent_id}"]
        }

    # --- EXECUTION WRAPPER ---

    async def run(self, task: str, user_id: str):
        """
        The main entry point used by main.py.
        Initializes state and invokes the async graph.
        """
        initial_state = {
            "task": task,
            "user_id": user_id,
            "history": [],
            "next_agent": "",
            "final_output": ""
        }
        
        # This triggers the full LangGraph lifecycle
        final_result = await self.graph.ainvoke(initial_state)
        return final_result
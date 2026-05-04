from agents.base_agent import BaseAgent

class GeneralAgent(BaseAgent):
    def __init__(self):
        super().__init__("General")

    def run(self, state: dict) -> dict:
        query = state["user_query"]
        prompt = (
            "You are a helpful legal assistant. Answer clearly in simple English.\n\n"
            f"Question: {query}\n\nAnswer:"
        )
        response = self._call_llm(prompt)
        return {"agent_response": response}

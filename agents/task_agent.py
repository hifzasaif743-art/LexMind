from agents.base_agent import BaseAgent

class TaskAgent(BaseAgent):
    def __init__(self):
        super().__init__("Task")

    def run(self, state: dict) -> dict:
        query = state["user_query"]
        context = state.get("retrieved_context") or ""
        prompt = (
            "You are a legal analyst. Perform the requested task on the provided context.\n"
            "If context is missing, answer based on the question alone.\n\n"
            f"CONTEXT:\n{context}\n\n"
            f"TASK:\n{query}\n\n"
            "Output in clear bullet points with headings when appropriate."
        )
        response = self._call_llm(prompt)
        return {"agent_response": response}

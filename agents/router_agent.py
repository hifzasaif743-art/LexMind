from agents.base_agent import BaseAgent

class RouterAgent(BaseAgent):
    def run(self, state: dict) -> dict:
        query = state["user_query"]
        prompt = "Classify this legal query into one word only: rag, general, or task.\n"
        prompt += "rag = question about a specific document\n"
        prompt += "general = general legal question\n"
        prompt += "task = extract clauses, summarize, list risks\n"
        prompt += "Query: " + query + "\nOne word answer:"
        result = self._call_llm(prompt).strip().lower()
        if result not in ["rag", "general", "task"]:
            result = "rag"
        print("[RouterAgent] Classified as: " + result)
        return {"query_type": result}
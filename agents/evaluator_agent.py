from agents.base_agent import BaseAgent

class EvaluatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Evaluator")

    def run(self, state: dict) -> dict:
        response = (state.get("agent_response") or "").strip()
        query = state.get("user_query") or ""

        if not response:
            return {"evaluation_result": "fail", "retry_count": state.get("retry_count", 0) + 1}

        prompt = (
            "You are a strict evaluator. Decide if the ANSWER adequately addresses the QUESTION.\n"
            "Reply with exactly one word: pass or fail.\n\n"
            f"QUESTION: {query}\n\n"
            f"ANSWER: {response}\n\n"
            "One word:"
        )
        verdict = self._call_llm(prompt).strip().lower()
        if verdict not in ("pass", "fail"):
            verdict = "pass"
        update = {"evaluation_result": verdict}
        if verdict == "fail":
            update["retry_count"] = state.get("retry_count", 0) + 1
        return update

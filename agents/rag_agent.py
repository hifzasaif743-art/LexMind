from agents.base_agent import BaseAgent
from rag.embeddings import FAISSVectorStore
import os

class RAGAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.vectorstore = FAISSVectorStore()
        index_path = "data/faiss_index"
        if os.path.exists(index_path):
            self.vectorstore.load(index_path)
    def run(self, state: dict) -> dict:
        query = state["user_query"]
        retry_count = state.get("retry_count", 0)
        context = self.vectorstore.search(query, k=4)
        if not context:
            context = "No relevant sections found."
        prompt = f"You are a legal analyst.\n\nCONTEXT:\n{context}\n\nQUESTION: {query}\n\nAnswer clearly, mark risks with [RISK]:"
        response = self._call_llm(prompt)
        return {"retrieved_context": context, "agent_response": response, "retry_count": retry_count}

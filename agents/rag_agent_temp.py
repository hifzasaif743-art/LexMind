from agents.base_agent import BaseAgent
from rag.embeddings import FAISSVectorStore

class RAGAgent(BaseAgent):
    def __init__(self):
        super().__init__("RAG")

    def process(self, query: str) -> str:

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

class Retriever:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        try:
            self.vector_store = FAISS.load_local("vector_store", self.embeddings)
        except Exception:
            self.vector_store = None

    def search(self, query: str, k: int = 3) -> str:
        if not self.vector_store:
            return "Vector store not found. Run the embeddings index creation first."
        docs = self.vector_store.similarity_search(query, k=k)
        return "\n\n".join(item.page_content for item in docs)

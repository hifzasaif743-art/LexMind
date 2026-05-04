# =============================================
# rag/embeddings.py
# Builds and searches the FAISS vector database
# =============================================

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List, Optional
import os


class FAISSVectorStore:
    """
    Manages the FAISS vector database.

    HOW IT WORKS:
    1. Takes text chunks from your PDF
    2. Converts each chunk to a vector (numbers) using HuggingFace model
    3. Stores all vectors in FAISS (fast similarity search)
    4. When you search, it finds the most similar chunks

    Uses HuggingFace 'all-MiniLM-L6-v2' - FREE, runs locally, no API key!
    """

    def __init__(self):
        print("[FAISSVectorStore] Loading embedding model (first time downloads ~90MB)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},  # Use CPU (change to "cuda" if you have GPU)
            encode_kwargs={"normalize_embeddings": True},
        )
        self.vectorstore: Optional[FAISS] = None
        print("[FAISSVectorStore] Embedding model ready.")

    def build(self, documents: List[Document], save_path: str = "data/faiss_index") -> None:
        """
        Builds FAISS index from document chunks and saves it to disk.
        Run this ONCE after loading your PDF.
        """
        if not documents:
            raise ValueError("No documents provided to build FAISS index!")

        print(f"[FAISSVectorStore] Building index from {len(documents)} chunks...")
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)

        # Create directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        self.vectorstore.save_local(save_path)
        print(f"[FAISSVectorStore] Index saved to: {save_path}")

    def load(self, load_path: str = "data/faiss_index") -> "FAISSVectorStore":
        """
        Loads a previously built FAISS index from disk.
        Call this every time you start the app.
        """
        if not os.path.exists(load_path):
            raise FileNotFoundError(
                f"FAISS index not found at '{load_path}'. "
                "Run setup_rag() in main.py first!"
            )

        self.vectorstore = FAISS.load_local(
            load_path,
            self.embeddings,
            allow_dangerous_deserialization=True,  # Required by FAISS
        )
        print(f"[FAISSVectorStore] Index loaded from: {load_path}")
        return self

    def search(self, query: str, k: int = 4) -> str:
        """
        Searches FAISS for the k most relevant chunks.
        Returns them as a single string joined by separators.
        """
        if self.vectorstore is None:
            return "ERROR: FAISS index not loaded. Call load() first."

        docs = self.vectorstore.similarity_search(query, k=k)

        if not docs:
            return "No relevant content found in the document."

        # Join chunks with separator for readability
        results = []
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "?")
            results.append(f"[Section {i+1} | Page {page} | Source: {os.path.basename(str(source))}]\n{doc.page_content}")

        return "\n\n---\n\n".join(results)

    def add_documents(self, documents: List[Document], save_path: str = "data/faiss_index") -> None:
        """Add new documents to an existing FAISS index."""
        if self.vectorstore is None:
            raise ValueError("Load an existing index first before adding documents.")

        self.vectorstore.add_documents(documents)
        self.vectorstore.save_local(save_path)
        print(f"[FAISSVectorStore] Added {len(documents)} new chunks. Index updated.")
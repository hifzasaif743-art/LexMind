# =============================================
# rag/document_loader.py
# Loads PDF files and splits them into chunks
# =============================================

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
import os


class LegalDocumentLoader:
    """
    Loads legal PDF documents and splits them into smaller chunks
    that FAISS can index and search efficiently.

    chunk_size=1000   → each chunk is ~1000 characters
    chunk_overlap=200 → chunks share 200 chars for context continuity
    """

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            # Legal documents have these natural separators
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )

    def load_pdf(self, pdf_path: str) -> List[Document]:
        """Load a single PDF and return chunked documents."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at: {pdf_path}")

        print(f"[DocumentLoader] Loading PDF: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        print(f"[DocumentLoader] Loaded {len(pages)} pages")

        chunks = self.splitter.split_documents(pages)
        print(f"[DocumentLoader] Split into {len(chunks)} chunks")
        return chunks

    def load_folder(self, folder_path: str) -> List[Document]:
        """Load ALL PDFs from a folder."""
        all_chunks = []
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

        if not pdf_files:
            raise ValueError(f"No PDF files found in: {folder_path}")

        for pdf_file in pdf_files:
            full_path = os.path.join(folder_path, pdf_file)
            chunks = self.load_pdf(full_path)
            all_chunks.extend(chunks)

        print(f"[DocumentLoader] Total chunks from all PDFs: {len(all_chunks)}")
        return all_chunks

    def load_text(self, text: str, source_name: str = "manual_input") -> List[Document]:
        """Load raw text directly (for testing without a PDF)."""
        doc = Document(page_content=text, metadata={"source": source_name})
        chunks = self.splitter.split_documents([doc])
        print(f"[DocumentLoader] Text split into {len(chunks)} chunks")
        return chunks
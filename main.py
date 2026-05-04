




import sys
import os
from dotenv import load_dotenv

_HERE = os.path.dirname(os.path.abspath(__file__))
# Always load LexMind/.env (not some other .env in the repo root)
load_dotenv(dotenv_path=os.path.join(_HERE, ".env"), override=True)

# ─── Configuration ─────────────────────────────────────────────────────────────
# Change this to your PDF file path (place PDFs in knowledge_base/)
PDF_PATH = "knowledge_base/your_document.pdf"
# FAISS index storage location (don't change unless needed)
FAISS_INDEX_PATH = "data/faiss_index"


# ─── Setup: Build FAISS index from PDF (run once) ──────────────────────────────
def setup_rag(pdf_path: str = PDF_PATH):
    """
    Run this ONCE to build the FAISS vector database from your PDF.
    After this, the index is saved and reloaded automatically.
    """
    from rag.document_loader import LegalDocumentLoader
    from rag.embeddings import FAISSVectorStore

    print("\n" + "="*50)
    print("  LexMind - Building RAG Index")
    print("="*50)

    if not os.path.exists(pdf_path):
        print(f"\n❌ ERROR: PDF not found at '{pdf_path}'")
        print("   Please add your PDF file to: knowledge_base/")
        print(f"   Then update PDF_PATH in main.py")
        return False

    # Load and chunk the PDF
    loader = LegalDocumentLoader(chunk_size=1000, chunk_overlap=200)
    documents = loader.load_pdf(pdf_path)

    # Build and save FAISS index
    store = FAISSVectorStore()
    store.build(documents, save_path=FAISS_INDEX_PATH)

    print("\n✅ RAG setup complete! You can now run queries.")
    print("   Run: python main.py\n")
    return True


# ─── Run a single query ────────────────────────────────────────────────────────
def run_query(user_query: str) -> str:
    """
    Main function to process a legal query through the multi-agent system.
    Returns the final response string.
    """
    from graph.workflow import build_graph

    # Build the LangGraph
    graph = build_graph()

    # Initialize state with all required fields
    initial_state = {
        "user_query": user_query,
        "query_type": "",
        "retrieved_context": None,
        "agent_response": None,
        "evaluation_result": None,
        "final_response": None,
        "messages": [],
        "retry_count": 0,
    }

    print(f"\n{'='*50}")
    print(f"  Query: {user_query}")
    print(f"{'='*50}")

    # Run the graph
    result = graph.invoke(initial_state)

    return result.get("final_response", "No response generated.")


# ─── Interactive Chat Mode ────────────────────────────────────────────────────
def chat_mode():
    """
    Interactive command-line chat with LexMind.
    Type 'quit' or 'exit' to stop.
    """
    print("\n" + "="*50)
    print("  ⚖️  LexMind - Legal Document Analyzer")
    print("  Powered by LangGraph + Groq (Llama 3.1)")
    print("="*50)
    print("\nCommands:")
    print("  Type your question and press Enter")
    print("  Type 'quit' to exit\n")

    # Check if FAISS index exists
    if not os.path.exists(FAISS_INDEX_PATH):
        print("⚠️  WARNING: No FAISS index found.")
        print("   RAG and Task queries won't work until you run:")
        print("   python main.py --setup\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break

            # Run the query
            response = run_query(user_input)

            print(f"\nLexMind:\n{response}\n")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\n\nGoodbye! ⚖️")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please check your .env file and try again.\n")


# ─── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Basic env check so fresh installs fail with a clear message
    if not (os.getenv("GROQ_API_KEY") or "").strip():
        print("\nERROR: Missing GROQ_API_KEY.")
        print("   Create a local .env (do NOT commit it) based on .env.example and set:")
        print("   GROQ_API_KEY=your_key_here\n")
        sys.exit(1)


    # python main.py --setup  → builds FAISS index from PDF
    if "--setup" in sys.argv:
        setup_rag(PDF_PATH)

    # python main.py --test  → runs 3 test queries and exits
    elif "--test" in sys.argv:
        test_queries = [
            "What is an NDA?",                          # general
            "Is there a penalty clause in this contract?",  # rag
            "Extract all clauses from the document",    # task
        ]
        for query in test_queries:
            response = run_query(query)
            print(f"\nLexMind: {response}\n")
            print("=" * 50)

    # python main.py  → start interactive chat
    else:
        chat_mode()

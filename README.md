LexMind — AI Legal Document Analyzer

 Multi-Agent AI system that analyzes legal contracts using LangGraph + RAG. Upload any PDF contract and get clause extraction, risk detection, and plain-English summaries — powered by Groq (Llama 3.1) and FAISS. 100% free to run.


🎯 What is LexMind?
Lawyers spend hours reading contracts. LexMind solves this.
Upload any legal PDF (contract, NDA, service agreement) and ask questions in plain English — or even Urdu. LexMind uses a multi-agent AI pipeline to:

🔍 Search your document for relevant clauses
⚠️ Highlight risky terms automatically
📋 Extract and list all clauses in structured format
📝 Summarize the entire contract in simple language
💬 Answer general legal questions without document lookup


🏗️ System Architecture
User Query (English / Urdu)
        │
        ▼
┌─────────────────┐
│  LangGraph State │  ← shared memory across all agents
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Router Agent   │  ← classifies query: rag / general / task
└────────┬────────┘
         │
    ┌────┴─────┬──────────┐
    ▼          ▼          ▼
┌───────┐ ┌─────────┐ ┌──────┐
│  RAG  │ │ General │ │ Task │
│ Agent │ │  Agent  │ │Agent │
└───┬───┘ └────┬────┘ └──┬───┘
    └──────────┴──────────┘
                │
                ▼
    ┌───────────────────────┐
    │    Evaluator Agent    │  ← quality check (pass / fail)
    └───────────┬───────────┘
                │
         ┌──────┴──────┐
         ▼             ▼
      PASS ✅       FAIL ❌
         │          (retry, max 3x)
         ▼
    Final Response
Agents
AgentRoleRouter AgentClassifies query into: rag, general, or taskRAG AgentSearches uploaded PDF using FAISS vector searchGeneral AgentAnswers general legal questions from LLM knowledgeTask AgentStructured extraction: clauses, risks, summariesEvaluator AgentQuality checks the response — retries if poor
Design Patterns Used

Router Pattern — query classification and routing
RAG Pattern — document retrieval with FAISS
Evaluator Pattern — answer quality control
Retry Loop — automatic retry on poor responses
Prompt Chaining — step-by-step agent pipeline


🛠️ Tech Stack
ToolPurposeCostLangGraphMulti-agent workflow orchestrationFREEGroq APILLM inference (Llama 3.1 8B)FREEFAISSLocal vector databaseFREEHuggingFace MiniLMLocal text embeddingsFREELangChainAI frameworkFREEPyPDFPDF loadingFREE

📁 Project Structure
LexMind/
├── agents/
│   ├── base_agent.py          # Abstract base class for all agents
│   ├── router_agent.py        # Query classifier
│   ├── rag_agent.py           # FAISS-powered document retrieval
│   ├── general_agent.py       # General legal Q&A
│   ├── task_agent.py          # Clause extraction & summarization
│   └── evaluator_agent.py     # Response quality checker
│
├── rag/
│   ├── document_loader.py     # PDF loader & text chunker
│   └── embeddings.py          # FAISS vector store manager
│
├── graph/
│   ├── state.py               # LangGraph shared state (TypedDict)
│   └── workflow.py            # Full agent pipeline with edges
│
├── utils/
│   └── prompts.py             # Centralized prompt templates
│
├── data/
│   └── documents/             # Place your PDF files here
│
├── .env                       # API keys (not committed)
├── requirements.txt
└── main.py                    # Entry point

⚡ Quick Start
1. Clone the repository
bashgit clone https://github.com/yourusername/LexMind.git
cd LexMind
2. Create virtual environment
bashpython -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
3. Install dependencies
bashpip install -r requirements.txt
4. Set up environment variables
Create a .env file in the root directory:
envGROQ_API_KEY=your_groq_api_key_here
Get your free Groq API key at console.groq.com
5. Add your PDF
Place your legal PDF in data/documents/ and update main.py:
pythonPDF_PATH = "data/documents/your_contract.pdf"
6. Build the vector index (run once)
bashpython main.py --setup
7. Start chatting
bashpython main.py

💬 Example Queries
You: What is the early termination penalty?
You: Extract all clauses from the document
You: What are my obligations under this agreement?
You: Summarize this contract in simple English
You: What does indemnity mean?
You: List all the risks in this contract
You: کیا اس معاہدے میں کوئی خطرناک شق ہے؟
Example Output
LexMind: Based on Section 4 of the agreement:

[⚠ RISK] Early Termination Penalty — If you exit the contract before
the end date without cause, you must pay a penalty equal to 3 months
of service fees ($15,000). This amount is due within 15 days of
sending the termination notice.

This is a HIGH RISK clause — the penalty is significant and the
payment window (15 days) is very short.

---
Analysis based on your uploaded document.

🔄 LangGraph State
All agents share a single state object:
pythonclass LegalAIState(TypedDict):
    user_query: str           # Original question
    query_type: str           # "rag" | "general" | "task"
    retrieved_context: str    # FAISS search results
    agent_response: str       # Raw agent answer
    evaluation_result: str    # "pass" | "fail"
    final_response: str       # Final output shown to user
    messages: List            # Conversation history
    retry_count: int          # Retry counter (max 3)

🐛 Troubleshooting
ErrorFixGROQ_API_KEY not foundCheck .env file has your keyFAISS index not foundRun python main.py --setup firstPDF not foundCheck PDF_PATH in main.py matches your filenameGroq rate limitWait 10 seconds — free tier has limitsHuggingFace download slowNormal on first run (~90MB, downloads once)No module named faissRun pip install faiss-cpu

🗺️ Roadmap

 Streamlit web UI
 Multi-document support
 Contract comparison feature
 Export analysis as PDF report
 Support for scanned PDFs (OCR)
 Urdu language full support


🤝 Contributing
Contributions are welcome! Please open an issue first to discuss what you would like to change.

Fork the repository
Create your feature branch: git checkout -b feature/AmazingFeature
Commit your changes: git commit -m 'Add AmazingFeature'
Push to the branch: git push origin feature/AmazingFeature
Open a Pull Request


📄 License
This project is licensed under the MIT License.

 Acknowledgements

LangChain for the AI framework
LangGraph for multi-agent orchestration
Groq for the blazing fast free LLM API
Facebook Research for FAISS

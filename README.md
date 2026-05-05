<div align="center">

# ⚖️ LexMind
### AI-Powered Legal Document Analyzer

**A production-grade Multi-Agent AI system that reads legal contracts and explains them in plain English.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.28-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://github.com/langchain-ai/langgraph)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.1-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://console.groq.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-0467DF?style=for-the-badge&logo=meta&logoColor=white)](https://github.com/facebookresearch/faiss)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)
[![Free](https://img.shields.io/badge/Cost-100%25_Free-gold?style=for-the-badge)]()

<br/>

> Lawyers spend hours reading contracts. **LexMind solves this in seconds.**

[Getting Started](#-quick-start) · [Architecture](#-system-architecture) · [Design Patterns](#-design-patterns) · [Evaluation](#-evaluation-criteria) · [Contributing](#-contributing)

</div>

---

## 📌 Business Scenario

Legal professionals and individuals spend hours manually reviewing contracts, NDAs, and service agreements. Missing a single risky clause can result in significant financial or legal consequences.

**LexMind** is an Agentic RAG system built for the legal domain. It allows users to upload any legal PDF and interact with it through natural language — getting clause extraction, risk analysis, plain-English summaries, and direct answers grounded in the actual document.

**Why it matters:** Legal AI is one of the fastest-growing sectors in enterprise software. This project demonstrates a real, deployable solution with genuine business value.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 PDF Upload | Supports any legal PDF — contracts, NDAs, service agreements |
| 🔍 Smart Retrieval | FAISS vector search finds the most relevant document sections |
| ⚠️ Risk Detection | Automatically flags HIGH / MEDIUM / LOW risk clauses |
| 📋 Clause Extraction | Structured list of all clauses with plain-English explanations |
| 🔄 Auto Retry | Evaluator agent retries automatically if answer quality is poor |
| 🌐 Multilingual | Supports both English and Urdu queries |
| 🆓 100% Free | Groq + FAISS + HuggingFace — zero cost to run |

---

## 🏗️ System Architecture

LexMind uses a **LangGraph-powered multi-agent pipeline**. Each agent has a single, well-defined responsibility following clean OOP design.

```
┌──────────────────────────────────────────────────────┐
│                     USER QUERY                        │
│               (English or Urdu)                       │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│                  LANGGRAPH STATE                      │
│  user_query · query_type · retrieved_context          │
│  agent_response · evaluation_result · retry_count     │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│                   ROUTER AGENT                        │
│          Classifies query into one of:                │
│          rag  ·  general  ·  task                     │
└───────┬──────────────┬──────────────┬────────────────┘
        │              │              │
        ▼              ▼              ▼
┌───────────┐   ┌───────────┐   ┌───────────┐
│    RAG    │   │  GENERAL  │   │   TASK    │
│   AGENT   │   │   AGENT   │   │   AGENT   │
│           │   │           │   │           │
│  FAISS    │   │  LLM      │   │ Extract   │
│  Search   │   │  Knowledge│   │ Summarize │
└─────┬─────┘   └─────┬─────┘   └─────┬─────┘
      │               │               │
      └───────────────┴───────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────┐
│                 EVALUATOR AGENT                       │
│          Quality check — PASS or FAIL                 │
│          Auto-retries up to 3 times if FAIL           │
└───────────────────────┬──────────────────────────────┘
                        │
               ┌────────┴────────┐
               │                 │
            PASS ✅           FAIL ❌
               │            (retry agent)
               ▼
┌──────────────────────┐
│    FINAL RESPONSE    │
└──────────────────────┘
```

### LangGraph Graph Design

| Component | Details |
|---|---|
| **Entry Point** | `router` node |
| **Nodes** | router · rag · general · task · evaluator · final |
| **Conditional Edge 1** | After `router` → routes to `rag`, `general`, or `task` based on `query_type` |
| **Conditional Edge 2** | After `evaluator` → routes to `final` on PASS, or back to agent on FAIL |
| **Fixed Edges** | `rag → evaluator`, `general → evaluator`, `task → evaluator`, `final → END` |
| **State** | `LegalAIState` TypedDict shared across all nodes |

### LangGraph Visualization (Mermaid)

```
graph TD
    router --> rag
    router --> general
    router --> task
    rag --> evaluator
    general --> evaluator
    task --> evaluator
    evaluator --> final
    evaluator --> rag
    evaluator --> general
    evaluator --> task
    final --> END
```

> To generate this visualization from code: `graph.get_graph().draw_mermaid()`

---

## 🎨 Design Patterns

| Pattern | Where Used | Why |
|---|---|---|
| **Router Pattern** | `RouterAgent` classifies every query | Separates concerns — each agent only handles what it is good at |
| **RAG Pattern** | `RAGAgent` + FAISS vector search | Grounds answers in real document content, prevents hallucination |
| **Evaluator Pattern** | `EvaluatorAgent` checks every response | Ensures quality control — poor answers are automatically retried |
| **Retry Loop** | `route_after_evaluator()` in workflow | Builds self-healing behavior into the pipeline |
| **Prompt Chaining** | State flows through nodes sequentially | Each node enriches the state before passing to the next |
| **OOP Inheritance** | All agents extend `BaseAgent` | Clean, extensible architecture — new agents take minutes to add |

---

## 🛠️ Tech Stack

| Tool | Version | Purpose | Cost |
|---|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | 0.2.28 | Multi-agent workflow orchestration | FREE |
| [LangChain](https://github.com/langchain-ai/langchain) | 0.2.16 | AI application framework | FREE |
| [Groq API](https://console.groq.com) | — | LLM inference — Llama 3.1 8B | FREE |
| [FAISS](https://github.com/facebookresearch/faiss) | 1.8.0 | Local vector similarity search | FREE |
| [HuggingFace MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | — | Local text embeddings (~90MB) | FREE |
| [PyPDF](https://pypdf.readthedocs.io) | 4.3.1 | PDF text extraction | FREE |
| [Python](https://python.org) | 3.11+ | Core language | FREE |

---

## 📁 Project Structure

```
LexMind/
│
├── .env                           # API keys (never commit)
├── .env.example                   # Template showing required keys
├── .gitignore                     # Ignores .env, __pycache__, venv/
├── requirements.txt               # All pip dependencies
├── README.md                      # This file
├── main.py                        # Entry point
│
├── agents/                        # All AI agents (OOP)
│   ├── __init__.py
│   ├── base_agent.py              # Abstract base class
│   ├── router_agent.py            # Query classifier
│   ├── rag_agent.py               # Document retrieval agent
│   ├── general_agent.py           # General Q&A agent
│   ├── task_agent.py              # Structured extraction agent
│   └── evaluator_agent.py         # Quality checker agent
│
├── rag/                           # RAG pipeline
│   ├── __init__.py
│   ├── document_loader.py         # PDF loader and chunker
│   └── embeddings.py              # FAISS vector store manager
│
├── graph/                         # LangGraph workflow
│   ├── __init__.py
│   ├── state.py                   # LegalAIState TypedDict
│   └── workflow.py                # Nodes, edges, conditional routing
│
├── utils/
│   ├── __init__.py
│   └── prompts.py                 # Centralized prompt templates
│
├── knowledge_base/                # Legal PDFs for RAG
│   ├── contract (2).pdf
│   ├── nda_template.pdf
│   └── service_agreement.pdf
│
└── data/
    └── faiss_index/               # Auto-generated vector index
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Free [Groq API key](https://console.groq.com) — no credit card needed

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/LexMind.git
cd LexMind
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
```
Then open `.env` and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

**5. Add your legal PDF to `knowledge_base/` and update `main.py`:**
```python
PDF_PATH = "knowledge_base/your_contract.pdf"
```

**6. Build FAISS index (run once per document)**
```bash
python main.py --setup
```

**7. Start LexMind**
```bash
python main.py
```

---

## 💬 Example Queries & Output

**RAG Query — searches the document:**
```
You: What is the early termination penalty?

LexMind: Based on Section 4 of the agreement:

[RISK] Early Termination — If you exit before the end date, you must
pay 3 months of service fees ($15,000) within 15 days of notice.

HIGH RISK: Large penalty with a very short payment window.
```

**Task Query — structured analysis:**
```
You: Extract all clauses and list the risks

LexMind:
KEY CLAUSES
- Clause 1 - Services: Software development and maintenance
- Clause 2 - Payment: $5,000/month, due within 30 days
- Clause 4 - Termination: 90 days notice required

RISK ANALYSIS
[HIGH]   Early exit penalty — $15,000
[HIGH]   Confidentiality breach — $50,000 damages
[MEDIUM] IP ownership — transfers only after full payment
```

**General Query — uses LLM knowledge:**
```
You: What does indemnification mean?

LexMind: Indemnification means one party agrees to cover the other's
losses or legal claims. In simple terms — if something goes wrong
because of your actions, you pay for it.
```

---

## 🗂️ LangGraph State Definition

```python
class LegalAIState(TypedDict):
    user_query: str            # Original user question
    query_type: str            # "rag" | "general" | "task"
    retrieved_context: str     # Document chunks from FAISS
    agent_response: str        # Raw answer from active agent
    evaluation_result: str     # "pass" | "fail"
    final_response: str        # Final output shown to user
    messages: List             # Full conversation history
    retry_count: int           # Retry counter (max 3)
```

---

## 📊 Evaluation Criteria

| Criteria | Weight | How LexMind Addresses It |
|---|---|---|
| **Code Quality & OOP** | 20% | All agents inherit from `BaseAgent`, clean naming, no hardcoded values, `.env` for secrets |
| **LangGraph Implementation** | 25% | Correct `TypedDict` state, 6 nodes, 2 conditional edges, compiles and runs end-to-end |
| **Design Patterns** | 15% | 6 patterns used: Router, RAG, Evaluator, Retry Loop, Prompt Chaining, OOP Inheritance |
| **Agentic RAG** | 20% | FAISS index built from PDFs, semantic search, answers grounded in document context |
| **Demo & Presentation** | 10% | Live CLI demo, clear architecture walkthrough, handles all 3 query types |
| **Innovation & Extras** | 10% | Urdu language support, auto-retry quality loop, structured task agent, evaluator pattern |

---

## 🐛 Troubleshooting

| Error | Fix |
|---|---|
| `GROQ_API_KEY not found` | Check `.env` file has your key |
| `FAISS index not found` | Run `python main.py --setup` first |
| `PDF not found` | Check `PDF_PATH` matches your filename exactly |
| `Rate limit error` | Wait 10 seconds — Groq free tier limit |
| `Slow first run` | Normal — HuggingFace model downloads once (~90MB) |
| `No module named faiss` | Run `pip install faiss-cpu` |

---

## 🗺️ Roadmap

- [x] Multi-agent LangGraph pipeline
- [x] FAISS vector search over legal PDFs
- [x] Automatic quality retry loop
- [x] English and Urdu query support
- [x] Structured clause and risk extraction
- [ ] Streamlit web UI
- [ ] Multi-document support
- [ ] Export analysis as PDF report
- [ ] OCR for scanned PDFs
- [ ] REST API endpoint

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "Add: your feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

All new agents must extend `BaseAgent` and implement the `run(self, state: dict) -> dict` method.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) · [LangGraph](https://github.com/langchain-ai/langgraph) · [Groq](https://groq.com) · [Facebook Research / FAISS](https://github.com/facebookresearch/faiss) · [HuggingFace](https://huggingface.co)

---

<div align="center">
Built with Python · LangGraph · Groq · FAISS
<br/><br/>
If you found this useful, please give it a ⭐
</div>

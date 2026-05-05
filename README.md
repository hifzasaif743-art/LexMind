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

[Getting Started](#-quick-start) · [Architecture](#-architecture) · [Features](#-features) · [Contributing](#-contributing)

</div>

---

## 📌 The Problem

Legal contracts are long, complex, and full of jargon. A single contract can take hours to review, and one missed clause can cost thousands of dollars. Most people sign contracts without fully understanding what they agreed to.

## ✅ The Solution

LexMind is a **multi-agent AI system** that:

- Reads any legal PDF you upload
- Finds and highlights risky clauses automatically
- Explains complex legal terms in plain English
- Extracts and organizes all clauses in structured format
- Answers questions about your specific contract
- Works in both **English and Urdu**

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 PDF Upload | Supports any legal PDF — contracts, NDAs, agreements |
| 🔍 Smart Search | FAISS vector search finds the most relevant sections |
| ⚠️ Risk Detection | Automatically flags high, medium, and low risk clauses |
| 📋 Clause Extraction | Lists all clauses in clean structured format |
| 💬 Plain English | Explains legal jargon in simple language |
| 🔄 Auto Retry | Evaluator agent retries if answer quality is poor |
| 🌐 Multilingual | Supports English and Urdu queries |
| 🆓 100% Free | Groq API + FAISS + HuggingFace — all free |

---

## 🏗️ Architecture

LexMind uses a **LangGraph-powered multi-agent pipeline** where each agent has a single responsibility.

```
┌─────────────────────────────────────────────────────┐
│                    USER QUERY                        │
│              (English or Urdu)                       │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                 LANGGRAPH STATE                      │
│   user_query · query_type · retrieved_context        │
│   agent_response · evaluation_result · retry_count   │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                  ROUTER AGENT                        │
│         Classifies query into one of:                │
│         rag  ·  general  ·  task                     │
└──────┬───────────────┬───────────────┬──────────────┘
       │               │               │
       ▼               ▼               ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│   RAG    │    │ GENERAL  │    │  TASK    │
│  AGENT   │    │  AGENT   │    │  AGENT   │
│          │    │          │    │          │
│ FAISS    │    │ LLM      │    │ Extract  │
│ Search   │    │ Knowledge│    │ Summarize│
└────┬─────┘    └────┬─────┘    └────┬─────┘
     │               │               │
     └───────────────┴───────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│               EVALUATOR AGENT                        │
│         Quality check: PASS or FAIL                  │
│         Auto-retries up to 3 times if FAIL           │
└──────────────────────┬──────────────────────────────┘
                       │
              ┌────────┴────────┐
              │                 │
           PASS ✅           FAIL ❌
              │                 │
              ▼           (retry agent)
┌─────────────────────┐
│    FINAL RESPONSE   │
│  Shown to the user  │
└─────────────────────┘
```

### Agent Responsibilities

| Agent | Role | Pattern Used |
|---|---|---|
| **Router Agent** | Reads query and classifies it as `rag`, `general`, or `task` | Router Pattern |
| **RAG Agent** | Searches PDF using FAISS, answers from document context | RAG Pattern |
| **General Agent** | Answers general legal questions using LLM knowledge | Direct Chain |
| **Task Agent** | Structured extraction: all clauses, risks, summary | Prompt Chaining |
| **Evaluator Agent** | Checks response quality, triggers retry if poor | Evaluator Pattern |

---

## 🛠️ Tech Stack

| Tool | Version | Purpose | Cost |
|---|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | 0.2.28 | Multi-agent workflow orchestration | FREE |
| [LangChain](https://github.com/langchain-ai/langchain) | 0.2.16 | AI application framework | FREE |
| [Groq API](https://console.groq.com) | - | LLM inference — Llama 3.1 8B | FREE |
| [FAISS](https://github.com/facebookresearch/faiss) | 1.8.0 | Local vector similarity search | FREE |
| [HuggingFace MiniLM](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | - | Local text embeddings (~90MB) | FREE |
| [PyPDF](https://pypdf.readthedocs.io) | 4.3.1 | PDF text extraction | FREE |
| [Python](https://python.org) | 3.11+ | Core language | FREE |

---

## 📁 Project Structure

```
LexMind/
│
├── agents/                        # All AI agents
│   ├── base_agent.py              # Abstract base class (OOP)
│   ├── router_agent.py            # Query classifier
│   ├── rag_agent.py               # Document retrieval agent
│   ├── general_agent.py           # General Q&A agent
│   ├── task_agent.py              # Structured extraction agent
│   ├── evaluator_agent.py         # Quality checker agent
│   └── __init__.py
│
├── rag/                           # RAG pipeline
│   ├── document_loader.py         # PDF loader and text chunker
│   ├── embeddings.py              # FAISS vector store manager
│   └── __init__.py
│
├── graph/                         # LangGraph workflow
│   ├── state.py                   # Shared state (TypedDict)
│   ├── workflow.py                # Nodes, edges, conditionals
│   └── __init__.py
│
├── utils/
│   ├── prompts.py                 # Centralized prompt templates
│   └── __init__.py
│
├── data/
│   ├── documents/                 # Place your PDF files here
│   └── faiss_index/               # Auto-generated vector index
│
├── .env                           # API keys (never commit this)
├── .gitignore
├── requirements.txt
├── README.md
└── main.py                        # Entry point
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.11+
- A free [Groq API key](https://console.groq.com)
- A legal PDF document to analyze

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/LexMind.git
cd LexMind
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install all dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at [console.groq.com](https://console.groq.com) — no credit card needed.

**5. Add your legal PDF**

Copy your PDF into `data/documents/` and update `main.py`:
```python
PDF_PATH = "data/documents/your_contract.pdf"
```

**6. Build the FAISS vector index (run once)**
```bash
python main.py --setup
```

**7. Start LexMind**
```bash
python main.py
```

---

## 💬 Example Output

```
You: What is the early termination penalty?

LexMind: Based on Section 4 of the agreement:

[RISK] Early Termination Penalty — If you exit the contract before
the end date without cause, you must pay a penalty equal to 3 months
of service fees ($15,000). This amount is due within 15 days of
sending the termination notice.

This is a HIGH RISK clause. The penalty is significant and the
payment window of 15 days is very short.
```

```
You: Extract all clauses from the document

LexMind:
KEY CLAUSES FOUND
- Clause 1 - Services: Company agrees to provide software development
- Clause 2 - Payment Terms: Client pays $5,000 per month
- Clause 3 - Duration: Agreement runs January to December 2025

RISK ANALYSIS
[HIGH RISK]   Early Termination — $15,000 penalty within 15 days
[HIGH RISK]   Confidentiality Breach — $50,000 in damages
[MEDIUM RISK] IP Ownership — transfers only after full payment
```

---

## 🗂️ LangGraph State

All agents share a single typed state object:

```python
class LegalAIState(TypedDict):
    user_query: str            # Original user question
    query_type: str            # "rag" | "general" | "task"
    retrieved_context: str     # Chunks found by FAISS search
    agent_response: str        # Raw answer from the agent
    evaluation_result: str     # "pass" | "fail"
    final_response: str        # Polished output shown to user
    messages: List             # Full conversation history
    retry_count: int           # Number of retries (max 3)
```

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `GROQ_API_KEY not found` | Missing .env | Check `.env` has your key |
| `FAISS index not found` | Setup not run | Run `python main.py --setup` |
| `PDF not found` | Wrong filename | Check `PDF_PATH` in `main.py` |
| `Rate limit error` | Groq free tier limit | Wait 10 seconds and retry |
| `Slow first run` | Model downloading | Normal — downloads once (~90MB) |
| `No module named faiss` | Missing package | Run `pip install faiss-cpu` |

---

## 🗺️ Roadmap

- [x] Multi-agent LangGraph pipeline
- [x] FAISS vector search
- [x] Automatic retry on poor responses
- [x] English and Urdu support
- [ ] Streamlit web UI
- [ ] Multi-document support
- [ ] Contract comparison feature
- [ ] Export analysis as PDF report
- [ ] OCR support for scanned PDFs
- [ ] REST API endpoint

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add: your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

All new agents must extend `BaseAgent` and implement the `run()` method.

---

## 📄 License

This project is licensed under the MIT License.

---

##  Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) for the AI framework
- [LangGraph](https://github.com/langchain-ai/langgraph) for multi-agent orchestration
- [Groq](https://groq.com) for fast free LLM inference
- [Facebook Research](https://github.com/facebookresearch/faiss) for FAISS
- [HuggingFace](https://huggingface.co) for the free embedding model

---

<div align="center">
Built with Python · LangGraph · Groq · FAISS
<br/>
If you found this useful, please give it a star
</div>

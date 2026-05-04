# LexMind (my-ai-assistant)

LexMind is a multi-agent legal document assistant built with LangGraph. It routes each user question to one of three paths—**general**, **rag** (document-grounded), or **task** (structured extraction/analysis)—then evaluates the answer before returning a final response.

## Install (PowerShell)

From the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configure environment variables

- **Do not commit** your real `.env`.
- Keep your real `.env` locally (same folder as `main.py`).
- Use `.env.example` as the template for GitHub.

Create your local `.env` like this:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and set `GROQ_API_KEY=...`.

## Where to put documents

Put your PDFs/TXTs in `knowledge_base/`.

If you want to build the RAG index, set `PDF_PATH` in `main.py` to point to **one PDF** in `knowledge_base/`, then run setup.

## Run

Interactive chat:

```powershell
python main.py
```

Build FAISS index (run once per document set):

```powershell
python main.py --setup
```

Quick demo test (runs 3 queries):

```powershell
python main.py --test
```

## Example questions (router demo)

- General: `What is an NDA?`
- RAG: `Is there a penalty clause in this contract?`
- Task: `Extract all clauses from the document`

## LangGraph visualization (Mermaid)

Print the Mermaid diagram:

```powershell
python scripts\graph_viz.py
```

Copy the Mermaid text into a Mermaid viewer (or Markdown preview that supports Mermaid) and take a screenshot for your report.

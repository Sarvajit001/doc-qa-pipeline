# Document Q&A Pipeline

A production-style RAG (Retrieval Augmented Generation) pipeline built from scratch
using Python, LangChain, and Flask. Supports multi-format documents, conversation
memory, vector store persistence, API authentication, and a tool-calling agent.

---

## What it does

Upload any document and ask questions about it. The system finds the most relevant
sections using semantic search and generates accurate answers using an LLM.
A separate agent endpoint adds tool-calling capabilities — dynamically choosing
between document search and a calculator depending on what the question needs.

---

## Tech Stack

- Python 3.10+
- LangChain + LangChain-Chroma
- ChromaDB (vector store, persisted to disk)
- HuggingFace Embeddings (sentence-transformers/all-MiniLM-L6-v2, runs locally)
- Groq LLM API (openai/gpt-oss-120b)
- Flask REST API
- SQLite (conversation history persistence)

---

## Project Structure
doc-qa/
├── app.py           → Flask API with all endpoints
├── pipeline.py      → RAG pipeline: loading, chunking, vector search, memory
├── agent.py         → Tool-calling agent: search_document + calculator tools
├── utils.py         → Original from-scratch version (no frameworks, for reference)
├── requirements.txt
├── .env             → API keys (never committed)
├── .gitignore
├── chroma_db/       → Persisted vector stores (auto-created, never committed)
├── conversations.db → SQLite history (auto-created, never committed)
└── sample.*         → Test documents (txt, pdf, xlsx, docx)

---

## Two Versions — Built Deliberately

This project was built twice on purpose.

**Version 1 — pure Python (utils.py + original pipeline.py)**
No frameworks. Manual file reading, manual chunking with a sliding window,
keyword matching for retrieval, direct Groq SDK calls. Every line written
from scratch to understand what each step actually does.

**Version 2 — LangChain (current pipeline.py + agent.py)**
Same pipeline rebuilt using LangChain components — TextLoader, RecursiveCharacterTextSplitter,
ChromaDB, HuggingFaceEmbeddings, ChatGroq, LCEL chain. Understanding the scratch
version first means I can explain exactly what LangChain is abstracting, not just
call a black box.

---

## API Endpoints

All endpoints require the `X-API-Key` header.

### POST /ask
Ask a question about a document. Maintains conversation history across turns via session ID.

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"question": "What is RAG?", "filepath": "sample.txt", "session_id": "session1"}'
```

Response:
```json
{
  "question": "What is RAG?",
  "answer": "RAG stands for Retrieval Augmented Generation...",
  "file": "sample.txt",
  "session_id": "session1"
}
```

### POST /agent
Tool-calling agent. Decides whether to search the document, use the calculator,
or answer directly — based on what the question actually needs.

```bash
curl -X POST http://localhost:5000/agent \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"question": "What is TypeScript and what is 3 times 7?", "filepath": "sample.docx"}'
```

Response:
```json
{
  "question": "What is TypeScript and what is 3 times 7?",
  "answer": "TypeScript is a typed superset of JavaScript. 3 x 7 = 21. Tools used: search_document, calculator."
}
```

### GET /history/\<session_id\>
View full conversation history for a session. Persisted to SQLite — survives server restarts.

```bash
curl http://localhost:5000/history/session1 \
  -H "X-API-Key: your_api_key"
```

### DELETE /clear/\<session_id\>
Clear conversation history for a session.

```bash
curl -X DELETE http://localhost:5000/clear/session1 \
  -H "X-API-Key: your_api_key"
```

---

## Supported File Formats

| Format | Loader used |
|--------|-------------|
| .txt | TextLoader |
| .pdf | PyPDFLoader |
| .docx | Docx2txtLoader |
| .xlsx / .xls | pandas + DataFrameLoader |

Adding a new format is one line in the LOADERS dictionary — no new elif blocks needed.

---

## How it works

### RAG Pipeline (/ask)
Document
→ load (TextLoader / PyPDFLoader / Docx2txtLoader / DataFrameLoader)
→ chunk (500 chars, 50 char overlap)
→ embed (HuggingFace all-MiniLM-L6-v2)
→ store in ChromaDB (persisted to disk, reused on repeat calls)
User question
→ embed with same model
→ semantic search in ChromaDB
→ top matching chunks retrieved
→ chunks + conversation history + question → LLM → answer
→ answer saved to SQLite for this session

### Tool-Calling Agent (/agent)
User question
↓
LLM reads question and decides:
→ search_document  (question relates to document content)
→ calculator       (question involves math or arithmetic)
→ neither          (general knowledge or refusal)
If search_document → retrieves relevant chunks via ChromaDB
If calculator      → evaluates math expression safely via eval()
Multi-step         → can call both tools in sequence on one question

### Vector Store Persistence

Documents are embedded once and saved under `./chroma_db/` using a key derived
from the file path + last-modified timestamp. On repeat questions, the existing
store loads from disk instantly. If the file changes, the timestamp changes, a
new key is generated, and it re-embeds automatically.

### Conversation Memory (/ask)

Each turn (question + answer) is written to SQLite immediately after generation.
On the next question in the same session, all prior turns are fetched and
formatted as plain text, then injected into the prompt so the LLM understands
follow-up references like "explain it simpler."

---

## Setup

### 1. Clone and create virtual environment

```bash
git clone git@github.com:Sarvajit001/doc-qa-pipeline.git
cd doc-qa-pipeline
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create .env file
GROQ_API_KEY=your_groq_api_key_here
API_KEY=your_chosen_api_key_here

Get a free Groq API key at https://console.groq.com

### 4. Run the server

```bash
python app.py
```

Server runs at http://localhost:5000

---

## Key Design Decisions

**Dispatch table for file loaders**
Instead of a long if/elif chain, a dictionary maps file extensions to their
loader classes. Adding a new file format is exactly one line in the dictionary.

**Tool binding via closure**
The agent's search_document tool has the filepath baked in at request time
via a closure. The LLM only needs to generate one argument (the question),
eliminating the multi-argument tool-call reliability issues that caused
intermittent crashes with the previous approach.

**Retry logic on agent tool calls**
Groq's LLaMA models occasionally return tool calls in a malformed text format
instead of the proper structured protocol. The agent catches these failures and
retries up to 2 times before returning a clean user-facing message.

**Model migration mid-project**
Discovered during testing that llama-3.3-70b-versatile was deprecated on Groq
(June 17, 2026). Researched Groq's deprecation docs, identified the recommended
replacement (openai/gpt-oss-120b), and migrated both /ask and /agent to the
new model. This resolved the tool-calling reliability issue entirely.

**Guardrails are per-endpoint, not global**
Each LLM-calling path has its own system prompt with its own guardrails.
Discovered during testing that /agent was generating code even though /ask
refused it — because the guardrail in pipeline.py only applies to that
specific code path. Fixed by adding explicit rules to the agent's own
system prompt. Lesson: guardrails are not global — every LLM call is a
blank slate unless you write rules into it explicitly.

---

## Known Limitations

| Limitation | Status |
|------------|--------|
| /agent has no conversation memory | Known gap — /ask has full SQLite memory, /agent is stateless |
| History grows unbounded on /ask | No sliding window yet — full transcript resent every turn |
| No per-user authentication | API key is single shared key, not per-user |
| Vector store rebuilt for new documents | Cached by file + timestamp, existing docs load from disk |

---

## What I would add next

- Conversation memory for /agent (session_id + SQLite, same pattern as /ask)
- Multi-document support (search across a folder, not just one file at a time)
- Simple HTML frontend so it can be demoed without curl
- Redis for conversation store in high-traffic production scenarios
- Proper user authentication with JWT for multi-user deployments

---

## Lessons learned

- Guardrails are not global — each LLM call needs its own rules in its own prompt
- Temperature matters for tool-calling — lower temperature = more consistent structured output
- Model deprecations happen in production — always watch provider changelogs
- Building from scratch before using a framework makes the framework make sense
- Testing with varied, adversarial inputs (wrong file format, out-of-document questions,
  code generation requests) reveals real gaps that happy-path testing misses

---

## Author

Sarvajit — built as a hands-on learning project to understand LLM pipelines,
RAG, agents, and production considerations from scratch.

GitHub: https://github.com/Sarvajit001/doc-qa-pipeline
# Folio

A chat interface for a Flask document-Q&A backend, with two modes:

- **Document mode** — calls `POST /ask`. Answers come strictly from the file you point it at (retrieval-augmented generation over that document).
- **Agent mode** — calls `POST /agent`. The backend searches and executes tools to answer, with or without a document in context.

Built with React, Vite, and Tailwind CSS. No backend code included here — this is the client for the Flask API in `app.py`.

## Why it's built this way

- **Mode is a first-class piece of state, not a URL param.** Each mode maps to a different backend route, a different accent color (teal for retrieval, amber for the agent), and different composer copy — so the interface tells you what kind of request you're about to send before you send it.
- **Session ID is explicit and visible.** The backend is stateful (`session_id` threads through history in SQLite), so the UI surfaces the session instead of hiding it — you can start a fresh one, reload a past one, or clear it.
- **Errors render as messages, not alerts.** A 404 for a bad filepath or a 401 for a missing API key shows up inline in the conversation, in plain language, so the flow never gets interrupted by a browser dialog.
- **Config lives in Settings, not in code.** API base URL and key are stored in `localStorage` and editable from the sidebar, so the same build works against a local server or a deployed one without a rebuild.

## Getting started

```bash
npm install
cp .env.example .env   # optional — Settings in the UI works without this
npm run dev
```

Open the printed local URL, then set your API base URL and key from **Connection settings** in the sidebar (defaults to `http://localhost:5000` with no key).

## Enable CORS on the Flask backend

The backend in the prompt doesn't set CORS headers. Since the UI runs on a different port than Flask, add this before running it locally:

```bash
pip install flask-cors
```

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # or CORS(app, origins=["http://localhost:5173"]) to restrict it
```

## Project structure

```
src/
  api.js               fetch wrapper for /ask, /agent, /history/:id, /clear/:id
  utils.js             session id, history normalization, small helpers
  App.jsx              state + layout root
  components/
    Sidebar.jsx         mode toggle, document path, session controls, settings
    Header.jsx          mobile menu trigger + current mode
    ChatPane.jsx         message list + empty state
    MessageBubble.jsx    user/assistant/error bubble styles
    Composer.jsx         input box, Enter-to-send
    ModeToggle.jsx        Document mode / Agent mode switch
```

## API contract this UI expects

| Method | Route | Body | Notes |
|---|---|---|---|
| POST | `/ask` | `{ question, filepath, session_id }` | RAG mode. 400/404 on bad input, 500 on pipeline errors. |
| POST | `/agent` | `{ question, filepath?, session_id }` | Agent mode. `filepath` is optional. |
| GET | `/history/:session_id` | — | Returns `{ session_id, history }`. |
| DELETE | `/clear/:session_id` | — | Clears stored history for that session. |

All requests send `X-API-Key` as a header.

## Build

```bash
npm run build
npm run preview
```

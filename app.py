from flask import Flask, request, jsonify
from pipeline import ask_question, get_history, clear_session_history
from agent import run_agent,get_conversation_history, clear_conversation_history
import uuid
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
VALID_API_KEY = os.getenv("API_KEY")


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not key or key != VALID_API_KEY:
            return jsonify({"error": "Unauthorized. Missing or invalid API key."}), 401
        return f(*args, **kwargs)
    return decorated


@app.route("/ask", methods=["POST"])
@require_api_key
def ask():
    data = request.get_json()
    if not data or "question" not in data or "filepath" not in data:
        return jsonify({"error": "Please provide question and filepath"}), 400

    question = data["question"]
    filepath = data["filepath"]
    session_id = data.get("session_id", str(uuid.uuid4()))

    # Check if file exists before doing anything
    if not os.path.exists(filepath):
        return jsonify({
            "error": f"File not found: '{filepath}'. Please check the filepath and try again."
        }), 404

    # Check if file format is supported
    ext = os.path.splitext(filepath)[1].lower()
    supported = [".txt", ".pdf", ".docx", ".xlsx", ".xls"]
    if ext not in supported:
        return jsonify({
            "error": f"Unsupported file type: '{ext}'. Supported formats: txt, pdf, docx, xlsx"
        }), 400

    try:
        answer = ask_question(filepath, question, session_id)
        return jsonify({
            "question": question,
            "answer": answer,
            "file": filepath,
            "session_id": session_id
        })
    except Exception as e:
        return jsonify({
            "error": f"Something went wrong: {str(e)}"
        }), 500


@app.route("/agent", methods=["POST"])
@require_api_key
def agent_ask():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "Please provide a question"}), 400

    question = data["question"]
    filepath = data.get("filepath")
    session_id = data.get("session_id", str(uuid.uuid4()))

    answer = run_agent(question, filepath=filepath, session_id=session_id)

    return jsonify({
        "question": question,
        "answer": answer,
        "session_id": session_id
    })


# @app.route("/history/<session_id>", methods=["GET"])
# @require_api_key
# def get_history_route(session_id):
#     history = get_history(session_id)
#     return jsonify({"session_id": session_id, "history": history})

@app.route("/history/<session_id>", methods=["GET"])
@require_api_key
def get_history_route(session_id):
    rag_turns = [
        {"question": h["question"], "answer": h["answer"], "mode": "rag"}
        for h in get_history(session_id)
    ]
    agent_turns = [
        {"question": h["user_input"], "answer": h["agent_response"], "mode": "agent"}
        for h in get_conversation_history(session_id)
    ]
    return jsonify({"session_id": session_id, "history": rag_turns + agent_turns})


# @app.route("/clear/<session_id>", methods=["DELETE"])
# @require_api_key
# def clear_history(session_id):
#     clear_session_history(session_id)
#     return jsonify({"message": "History cleared", "session_id": session_id})

@app.route("/clear/<session_id>", methods=["DELETE"])
@require_api_key
def clear_history(session_id):
    clear_session_history(session_id)
    clear_conversation_history(session_id)
    return jsonify({"message": "History cleared", "session_id": session_id})


if __name__ == "__main__":
    app.run(debug=True)
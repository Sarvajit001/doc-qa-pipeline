from flask import Flask, request, jsonify
from pipeline import ask_question, get_history, clear_session_history
import uuid
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)

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

    answer = ask_question(filepath, question, session_id)

    return jsonify({
        "question": question,
        "answer": answer,
        "file": filepath,
        "session_id": session_id
    })


@app.route("/history/<session_id>", methods=["GET"])
@require_api_key
def get_history_route(session_id):
    history = get_history(session_id)
    return jsonify({"session_id": session_id, "history": history})


@app.route("/clear/<session_id>", methods=["DELETE"])
@require_api_key
def clear_history(session_id):
    clear_session_history(session_id)
    return jsonify({"message": "History cleared", "session_id": session_id})


if __name__ == "__main__":
    app.run(debug=True)
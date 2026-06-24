from flask import Flask, request, jsonify
from pipeline import ask_question
import uuid

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
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
def get_history(session_id):
    from pipeline import conversation_store
    history = conversation_store.get(session_id, [])
    return jsonify({"session_id": session_id, "history": history})

@app.route("/clear/<session_id>", methods=["DELETE"])
def clear_history(session_id):
    from pipeline import conversation_store
    if session_id in conversation_store:
        del conversation_store[session_id]
    return jsonify({"message": "History cleared", "session_id": session_id})

if __name__ == "__main__":
    app.run(debug=True)
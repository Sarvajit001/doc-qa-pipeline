from flask import Flask, request, jsonify
from pipeline import ask_question

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    
    if not data or "question" not in data or "filepath" not in data:
        return jsonify({"error": "Please provide question and filepath"}), 400
    
    question = data["question"]
    filepath = data["filepath"]
    
    answer = ask_question(filepath, question)
    
    return jsonify({
        "question": question,
        "answer": answer,
        "file": filepath
    })

if __name__ == "__main__":
    app.run(debug=True)
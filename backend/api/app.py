from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.abspath("../app"))

from rag_engine import RAGEngine


app = Flask(__name__)
rag = RAGEngine()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Missing 'question'"}), 400

    try:
        answer = rag.ask(question)
        return jsonify({"question": question, "answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

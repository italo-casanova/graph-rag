from flask import Flask, request, jsonify

from retrieval.hybrid_search import hybrid_search
from llm.bedrock_client import generate_answer

app = Flask(__name__)


@app.route("/query", methods=["POST"])
def query():

    question = request.json["question"]

    context = hybrid_search(question)

    answer = generate_answer(context, question)

    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(port=5000)

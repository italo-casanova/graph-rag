from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
import time

from retrieval.hybrid_search import hybrid_search
from llm.bedrock_client import generate_answer
from logger import setup_root_logger, get_logger

# setup logging
setup_root_logger()
logger = get_logger("app")

app = Flask(__name__)


@app.before_request
def before_request():
    request.start_time = time.time()
    logger.info(f"➡️  {request.method} {request.path}")


@app.after_request
def after_request(response):
    duration = time.time() - getattr(request, "start_time", time.time())
    logger.info(
        f" {request.method} {request.path} {response.status_code} ({duration:.3f}s)"
    )
    return response


@app.route("/query", methods=["POST"])
@app.route("/query/", methods=["POST"])
def query():

    data = request.get_json(force=True, silent=True)

    if not data or "question" not in data:
        logger.warning("Missing question in request")
        return jsonify({"error": "missing question"}), 400

    question = data["question"]

    logger.info(f"Processing query: {question}")

    context = hybrid_search(question)

    logger.info(f"Retrieved context size: {len(context)}")

    answer = generate_answer(context, question)

    logger.info("Answer generated successfully")

    return jsonify({"answer": answer})


@app.route("/health", methods=["GET"])
@app.route("/health/", methods=["GET"])
def health():
    logger.info(" Health check OK")
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    logger.info("Running locally with Flask")
    app.run(host="0.0.0.0", port=5000)

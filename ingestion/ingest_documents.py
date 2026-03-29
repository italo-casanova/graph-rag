import os
import uuid
import logging
import re

from ingestion.pdf_parser import parse_pdf
from ingestion.chunker import chunk_text
from ingestion.embedder import embed

from db.postgres import get_connection, release_connection
from graph.graph_operations import insert_document_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingestion")

DATA_DIR = "data"


def clean_text(text):
    if not text:
        return ""

    text = text.replace("\x00", "")
    text = re.sub(r"[\x00-\x1f]+", " ", text)

    return text.strip()


def infer_concept(file_path):
    """
    Normalizado a español (clave para matching con LLM)
    """

    path = file_path.lower()

    if "contracts" in path:
        return "contrato"

    if "regulatory" in path:
        return "regulación"

    if "invoices" in path:
        return "factura"

    if "proposals" in path:
        return "propuesta"

    return "documento"


def ingest_pdf(file_path):

    try:
        doc_id = str(uuid.uuid4())
        concept = infer_concept(file_path)

        logger.info(f"Ingesting {file_path} as concept {concept}")

        text = parse_pdf(file_path)
        text = clean_text(text)

        chunks = chunk_text(text)

        logger.info(f"Total chunks: {len(chunks)}")

        conn = get_connection()
        cur = conn.cursor()

        # 🔥 grafo con concepto NORMALIZADO
        insert_document_graph(doc_id, concept)

        for i, chunk in enumerate(chunks):

            chunk = clean_text(chunk)

            if not chunk:
                continue

            logger.info(f"Embedding chunk {i+1}/{len(chunks)}")

            embedding = embed(chunk)

            vector = "[" + ",".join(map(str, embedding)) + "]"

            cur.execute(
                """
                INSERT INTO documents (doc_id, text, embedding)
                VALUES (%s, %s, %s::vector)
                """,
                (doc_id, chunk, vector),
            )

        conn.commit()
        release_connection(conn)

        logger.info(f"Ingestion finished for {file_path}")

    except Exception as e:
        logger.exception(f"Error ingesting {file_path}")


def ingest_all():

    logger.info(f"Scanning directory {DATA_DIR}")

    for root, _, files in os.walk(DATA_DIR):

        for file in files:

            if not file.lower().endswith(".pdf"):
                continue

            path = os.path.join(root, file)
            ingest_pdf(path)


if __name__ == "__main__":
    ingest_all()

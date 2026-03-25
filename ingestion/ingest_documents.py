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
    """
    Remove problematic characters extracted from PDFs
    """

    if text is None:
        return ""

    # remove null bytes
    text = text.replace("\x00", "")

    # remove other control characters
    text = re.sub(r"[\x00-\x1f]+", " ", text)

    return text.strip()


def infer_concept(file_path):
    """
    Automatically infer graph concept from directory
    """

    if "contracts" in file_path.lower():
        return "Contract"

    if "regulatory" in file_path.lower():
        return "Regulation"

    if "invoices" in file_path.lower():
        return "Invoice"

    if "proposals" in file_path.lower():
        return "Proposal"

    return "Document"


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

        # 🔥 solo metadata ligera en grafo
        insert_document_graph(doc_id, concept)

        for i, chunk in enumerate(chunks):

            chunk = clean_text(chunk)

            if not chunk.strip():
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

        logger.error(f"Error ingesting {file_path}: {e}")


def ingest_all():

    logger.info(f"Scanning directory {DATA_DIR}")

    found_files = 0

    for root, _, files in os.walk(DATA_DIR):

        logger.info(f"Entering directory: {root}")

        for file in files:

            logger.info(f"Found file: {file}")

            if not file.lower().endswith(".pdf"):
                logger.info(f"Skipping non-pdf file: {file}")
                continue

            found_files += 1

            path = os.path.join(root, file)

            ingest_pdf(path)

    if found_files == 0:
        logger.warning("No PDF files found in data directory")


if __name__ == "__main__":

    ingest_all()


from ingestion.pdf_parser import parse_pdf
from ingestion.chunker import chunk_text
from ingestion.embedder import embed

from db.postgres import get_connection, release_connection
from graph.graph_operations import create_concept, insert_document_graph

from logger import get_logger

logger = get_logger("ingestion")


def ingest(pdf_path, doc_id, concept):

    logger.info(f"Starting ingestion for {pdf_path}")

    text = parse_pdf(pdf_path)

    logger.info("PDF parsed")

    chunks = chunk_text(text)

    logger.info(f"Generated {len(chunks)} chunks")

    create_concept(concept)

    logger.info(f"Concept '{concept}' ensured in graph")

    conn = get_connection()
    cur = conn.cursor()

    for i, chunk in enumerate(chunks):

        logger.info(f"Embedding chunk {i+1}/{len(chunks)}")

        embedding = embed(chunk)

        cur.execute(
            """
            INSERT INTO documents(text, embedding)
            VALUES(%s,%s)
            """,
            (chunk, embedding),
        )

        logger.info(f"Stored vector for chunk {i+1}")

        insert_document_graph(doc_id, concept, chunk)

        logger.info(f"Inserted graph node for chunk {i+1}")

    conn.commit()

    logger.info("Postgres commit completed")

    release_connection(conn)

    logger.info(f"Ingestion completed for {pdf_path}")


if __name__ == "__main__":

    ingest("data/raee.pdf", "doc_raee", "RAEE")

    ingest("data/arrendamiento.pdf", "doc_arrendamiento", "Arrendamiento")

import logging

from ingestion.embedder import embed
from retrieval.entity_extractor import extract_entities
from retrieval.graph_search import search_graph
from retrieval.vector_search import search_vector

logger = logging.getLogger("hybrid")


def hybrid_search(query, k=10):

    logger.info("Starting hybrid search")

    # --- entities ---
    entities = extract_entities(query)
    logger.info(f"Entities: {entities}")

    # --- graph ---
    doc_ids = search_graph(entities)
    logger.info(f"Graph docs: {len(doc_ids)}")

    # --- embedding ---
    embedding = embed(query)

    # --- ranking ---
    if doc_ids:
        logger.info("Using graph-filtered search")
        results = search_vector(embedding, doc_ids, k)
    else:
        logger.warning("⚠️ Graph empty → fallback vector search")
        results = search_vector(embedding, None, k)

    logger.info(f"Final results: {len(results)}")

    return results


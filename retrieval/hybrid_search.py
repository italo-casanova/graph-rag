import logging

from ingestion.embedder import embed
from retrieval.entity_extractor import extract_entities
from retrieval.graph_search import search_graph
from retrieval.vector_search import search_vector


logger = logging.getLogger("hybrid")


def hybrid_search(query, k=10):
    """
    Hybrid retrieval pipeline:

    1. Extract entities from query
    2. Retrieve candidate documents from graph
    3. Rank documents using vector similarity
    """

    logger.info("Starting hybrid search")

    # --- entity extraction ---
    entities = extract_entities(query)

    logger.info(f"Extracted entities: {entities}")

    # --- graph retrieval ---
    doc_ids = search_graph(entities)

    logger.info(f"Graph returned {len(doc_ids)} candidate documents")

    # --- vector embedding ---
    embedding = embed(query)

    # --- vector ranking ---
    if doc_ids:
        logger.info("Running filtered vector search")

        results = search_vector(embedding, doc_ids, k)

    else:
        logger.info("No graph candidates → fallback to pure vector search")

        results = search_vector(embedding, None, k)

    logger.info(f"Retrieved {len(results)} results")

    return results
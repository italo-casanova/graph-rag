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

    concepts = entities.get("concepts", [])
    keywords = entities.get("keywords", [])

    logger.info(f"Concepts: {concepts}")
    logger.info(f"Keywords: {keywords}")

    # --- graph search (SOLO concepts) ---
    doc_ids = search_graph(concepts)
    logger.info(f"Graph docs: {len(doc_ids)}")

    # --- query enhancement ---
    enhanced_query = query
    if keywords:
        enhanced_query = query + " " + " ".join(keywords)
        logger.info(f"Enhanced query: {enhanced_query}")

    # --- embedding ---
    embedding = embed(enhanced_query)

    # --- ranking ---
    if doc_ids:
        logger.info("Using graph-filtered vector search")
        results = search_vector(embedding, doc_ids, k)

        # 🔥 fallback inteligente si el grafo filtra demasiado
        if not results:
            logger.warning(
                "⚠️ Graph filter too strict → fallback to full vector search"
            )
            results = search_vector(embedding, None, k)

    else:
        logger.warning("⚠️ Graph empty → fallback vector search")
        results = search_vector(embedding, None, k)

    logger.info(f"Final results: {len(results)}")

    return results

from ingestion.embedder import embed

from retrieval.vector_search import search_vector
from retrieval.graph_search import search_graph


def hybrid_search(query):

    embedding = embed(query)

    vector_results = search_vector(embedding)

    graph_results = search_graph(query)

    return vector_results + graph_results

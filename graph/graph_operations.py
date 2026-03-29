from graph.graph_client import submit_query


def _sanitize(text: str) -> str:
    if not text:
        return ""
    return text.replace("'", " ").strip()


def _concept_id(concept: str) -> str:
    return f"concept::{_sanitize(concept)}"


def _document_id(doc_id: str) -> str:
    return f"doc::{doc_id}"


def insert_document_graph(doc_id: str, concept: str):
    """
    Insert document + concept + edge (safe for Neptune memory)
    """

    concept = _sanitize(concept)

    concept_id = _concept_id(concept)
    document_id = _document_id(doc_id)

    # 1. Ensure concept exists
    submit_query(f"""
    g.V('{concept_id}')
      .fold()
      .coalesce(
          unfold(),
          addV('Concept')
            .property(id,'{concept_id}')
            .property('name','{concept}')
      )
    """)

    # 2. Ensure document exists
    submit_query(f"""
    g.V('{document_id}')
      .fold()
      .coalesce(
          unfold(),
          addV('Document')
            .property(id,'{document_id}')
            .property('doc_id','{doc_id}')
      )
    """)

    # 3. Create edge (NO heavy check)
    submit_query(f"""
    g.V('{concept_id}')
      .addE('mentions')
      .to(g.V('{document_id}'))
    """)


def get_documents_by_concept(concept: str, limit: int = 5):

    concept_id = _concept_id(concept)

    query = f"""
    g.V('{concept_id}')
      .out('mentions')
      .values('doc_id')
      .limit({limit})
    """

    return submit_query(query)


def get_concepts_by_document(doc_id: str):

    document_id = _document_id(doc_id)

    query = f"""
    g.V('{document_id}')
      .in('mentions')
      .values('name')
    """

    return submit_query(query)


def get_all_documents(limit=50):

    query = f"""
    g.V().hasLabel('Document')
      .values('doc_id')
      .limit({limit})
    """

    return submit_query(query)


def get_all_concepts(limit=50):

    query = f"""
    g.V().hasLabel('Concept')
      .values('name')
      .limit({limit})
    """

    return submit_query(query)


def count_vertices():
    return submit_query("g.V().count()")


def count_edges():
    return submit_query("g.E().count()")


def graph_summary():
    return {
        "vertices": submit_query("g.V().count()"),
        "edges": submit_query("g.E().count()"),
        "concepts": submit_query("g.V().hasLabel('Concept').count()"),
        "documents": submit_query("g.V().hasLabel('Document').count()"),
    }


def delete_document(doc_id: str):

    document_id = _document_id(doc_id)

    query = f"""
    g.V('{document_id}')
      .drop()
    """

    return submit_query(query)


def delete_concept(concept: str):

    concept_id = _concept_id(concept)

    query = f"""
    g.V('{concept_id}')
      .drop()
    """

    return submit_query(query)


def clear_graph():
    return submit_query("g.V().drop()")

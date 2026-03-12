from graph.graph_client import submit_query


def insert_document_graph(doc_id, concept):
    """
    Insert document and concept and connect them safely
    """

    concept = concept.replace("'", " ")

    query = f"""
    g.V().has('Concept','name','{concept}')
      .fold()
      .coalesce(
          unfold(),
          addV('Concept').property('name','{concept}')
      ).as('c')
      .V().has('Document','doc_id','{doc_id}')
      .fold()
      .coalesce(
          unfold(),
          addV('Document').property('doc_id','{doc_id}')
      ).as('d')
      .coalesce(
          __.select('c').outE('mentions').where(inV().as('d')),
          __.select('c').addE('mentions').to('d')
      )
    """

    submit_query(query)


def get_documents_by_concept(concept, limit=5):
    """
    Retrieve documents linked to a concept
    """

    concept = concept.replace("'", " ")

    query = f"""
    g.V().has('Concept','name','{concept}')
      .out('mentions')
      .values('doc_id')
      .dedup()
      .limit({limit})
    """

    return submit_query(query)


def count_vertices():
    """
    Debug helper
    """

    return submit_query("g.V().count()")
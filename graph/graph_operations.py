from graph.graph_client import submit_query


def create_concept(concept):

    concept = concept.replace("'", " ")

    query = f"""
    g.V().has('Concept','name','{concept}')
      .fold()
      .coalesce(
          unfold(),
          addV('Concept').property('name','{concept}')
      )
    """

    submit_query(query)


def insert_document_graph(doc_id, concept, text):

    text = text.replace("'", " ")

    query_doc = f"""
    g.V().has('Document','doc_id','{doc_id}')
      .fold()
      .coalesce(
        unfold(),
        addV('Document').property('doc_id','{doc_id}')
      )
    """

    submit_query(query_doc)

    query_concept = f"""
    g.V().has('Concept','name','{concept}')
      .fold()
      .coalesce(
        unfold(),
        addV('Concept').property('name','{concept}')
      )
    """

    submit_query(query_concept)

    query_chunk = f"""
    g.addV('Chunk')
      .property('text','{text}')
    """

    submit_query(query_chunk)

    # SAFE edge creation
    query_edge = f"""
    g.V().has('Document','doc_id','{doc_id}').limit(1).as('d')
     .V().has('Concept','name','{concept}').limit(1)
     .addE('mentions').from('d')
    """

    submit_query(query_edge)


def get_documents_by_concept(concept, limit=5):

    concept = concept.replace("'", " ")

    query = f"""
    g.V().has('Concept','name','{concept}')
      .in('mentions')
      .values('text')
      .limit({limit})
    """

    return submit_query(query)


def count_vertices():

    return submit_query("g.V().count()")

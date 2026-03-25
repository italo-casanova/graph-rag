from graph.graph_client import submit_query


def concept_exists(concept_id):
    result = submit_query(f"g.V('{concept_id}').limit(1)")
    return len(result) > 0


def create_concept(concept_id, concept):
    submit_query(f"""
    g.addV('Concept')
     .property(id,'{concept_id}')
     .property('name','{concept}')
    """)


def create_document(document_id, doc_id):
    submit_query(f"""
    g.addV('Document')
     .property(id,'{document_id}')
     .property('doc_id','{doc_id}')
    """)


def create_edge(concept_id, document_id):
    submit_query(f"""
    g.V('{concept_id}')
     .addE('mentions')
     .to(g.V('{document_id}'))
    """)


def insert_document_graph(doc_id, concept):

    concept = concept.replace("'", " ")

    concept_id = f"concept::{concept}"
    document_id = f"doc::{doc_id}"

    query = f"""
    g.addV('Document')
     .property(id,'{document_id}')
     .property('doc_id','{doc_id}')
     .as('d')
     .V('{concept_id}')
     .fold()
     .coalesce(
        unfold(),
        addV('Concept')
          .property(id,'{concept_id}')
          .property('name','{concept}')
     )
     .addE('mentions')
     .to('d')
    """

    submit_query(query)


def get_documents_by_concept(concept, limit=5):

    concept = concept.replace("'", " ")
    concept_id = f"concept::{concept}"

    query = f"""
    g.V('{concept_id}')
      .out('mentions')
      .values('doc_id')
      .limit({limit})
    """

    return submit_query(query)


def count_vertices():
    return submit_query("g.V().count()")

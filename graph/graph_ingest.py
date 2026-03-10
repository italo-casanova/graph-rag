from graph.graph_client import submit_query


def create_document(doc_id, title):

    query = f"""
    g.addV('Document')
    .property('doc_id','{doc_id}')
    .property('title','{title}')
    """

    submit_query(query)


def create_entity(label, name):

    query = f"""
    g.V().has('{label}','name','{name}')
    .fold()
    .coalesce(
        unfold(),
        addV('{label}').property('name','{name}')
    )
    """

    submit_query(query)


def link_document(doc_id, label, name, relation):

    query = f"""
    g.V().has('Document','doc_id','{doc_id}')
    .addE('{relation}')
    .to(
        g.V().has('{label}','name','{name}')
    )
    """

    submit_query(query)

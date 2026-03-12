from graph.graph_client import submit_query


def search_graph(concepts, limit=10):
    """
    Retrieve documents connected to concepts in the graph.
    Uses multi-hop traversal for better recall.
    """

    if not concepts:
        return []

    # sanitize
    concepts = [c.replace("'", "") for c in concepts]

    concept_list = ",".join([f'"{c}"' for c in concepts])

    gremlin = f"""
    g.V()
      .hasLabel('Concept')
      .has('name', within({concept_list}))
      .as('c')

      .union(
          __.in('mentions'),          // direct documents
          __.both().in('mentions')    // related concepts → documents
      )

      .hasLabel('Document')
      .values('doc_id')
      .dedup()
      .limit({limit})
    """

    return submit_query(gremlin)
import logging
from graph.graph_client import get_client

NEPTUNE_ENDPOINT = "wss://db-neptune-3-instance-1.cecua5pujewa.us-east-1.neptune.amazonaws.com:8182/gremlin"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("explorer")


def run_query(g, query):
    logger.info(f"\nExecuting:\n{query}")
    result = g.submit(query).all().result()
    for r in result:
        print(r)
    return result


def list_vertices(g):
    print("\n=== ALL VERTICES ===")
    query = """
    g.V().project('id','label','props')
      .by(id)
      .by(label)
      .by(valueMap())
    """
    run_query(g, query)


def list_edges(g):
    print("\n=== ALL EDGES ===")
    query = """
    g.E().project('id','label','from','to')
      .by(id)
      .by(label)
      .by(outV().id())
      .by(inV().id())
    """
    run_query(g, query)


def show_graph(g):
    print("\n=== GRAPH RELATIONSHIPS ===")
    query = """
    g.V().as('v')
      .outE('mentions').as('e')
      .inV().as('d')
      .select('v','e','d')
      .by(id)
    """
    run_query(g, query)


def show_document(g, doc_id):
    print(f"\n=== DOCUMENT {doc_id} ===")
    query = f"""
    g.V('doc::{doc_id}')
      .project('id','label','props','concepts')
      .by(id)
      .by(label)
      .by(valueMap())
      .by(in('mentions').values('name'))
    """
    run_query(g, query)


def show_concept(g, concept):
    print(f"\n=== CONCEPT {concept} ===")
    query = f"""
    g.V('concept::{concept}')
      .project('id','docs')
      .by(id)
      .by(out('mentions').id())
    """
    run_query(g, query)


if __name__ == "__main__":
    g = get_client()

    try:
        list_vertices(g)
        list_edges(g)
        show_graph(g)

        # 👇 prueba con uno real
        show_document(g, "d78dfaaa-ab90-4d80-a1fc-1cb42a172545")
        show_concept(g, "propuesta")

    finally:
        g.close()

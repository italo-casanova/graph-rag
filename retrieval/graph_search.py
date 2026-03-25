from graph.graph_client import submit_query
import logging

logger = logging.getLogger("graph_search")


def search_graph(entities, per_entity_limit=5, global_limit=20):

    if not entities:
        return []

    doc_ids = set()

    for entity in entities:

        concept_id = f"concept::{entity}"

        query = f"""
        g.V('{concept_id}')
         .out('mentions')
         .limit({per_entity_limit})
         .values('doc_id')
        """

        try:
            results = submit_query(query)

            for r in results:
                doc_ids.add(r)

                if len(doc_ids) >= global_limit:
                    return list(doc_ids)

        except Exception as e:
            logger.warning(f"Graph query failed for {entity}: {e}")
            continue

    return list(doc_ids)

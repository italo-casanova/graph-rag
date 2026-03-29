from graph.graph_client import submit_query
import logging

logger = logging.getLogger("graph_search")


ENTITY_TO_CONCEPT = {
    "contrato": "Contract",
    "adenda": "Contract",
    "anticorrupcion": "Contract",
    "propuesta": "Proposal",
    "cotizacion": "Proposal",
    "licencias": "Proposal",
    "factura": "Invoice",
    "regulacion": "Regulation",
    "ley": "Regulation",
}


def map_entity_to_concept(entity):

    for key in ENTITY_TO_CONCEPT:
        if key in entity:
            return ENTITY_TO_CONCEPT[key]

    return None


def search_graph(entities, per_entity_limit=5, global_limit=20):

    if not entities:
        return []

    doc_ids = set()

    for entity in entities:

        concept = map_entity_to_concept(entity)

        if not concept:
            continue

        concept_id = f"concept::{concept}"

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

    return list(doc_ids)

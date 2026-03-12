from db.postgres import get_connection, release_connection


def search_vector(embedding, doc_ids=None, limit=5):

    conn = get_connection()
    cur = conn.cursor()

    vector = "[" + ",".join(str(x) for x in embedding) + "]"

    if doc_ids:

        placeholders = ",".join(["%s"] * len(doc_ids))

        query = f"""
        SELECT text
        FROM documents
        WHERE doc_id IN ({placeholders})
        ORDER BY embedding <=> '{vector}'::vector
        LIMIT {limit}
        """

        cur.execute(query, doc_ids)

    else:

        query = f"""
        SELECT text
        FROM documents
        ORDER BY embedding <=> '{vector}'::vector
        LIMIT {limit}
        """

        cur.execute(query)

    results = cur.fetchall()

    release_connection(conn)

    return [r[0] for r in results]
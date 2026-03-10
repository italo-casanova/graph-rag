from db.postgres import get_connection, release_connection


def search_vector(embedding):

    conn = get_connection()
    cur = conn.cursor()

    # convert embedding to pgvector string
    vector = "[" + ",".join(str(x) for x in embedding) + "]"

    query = f"""
        SELECT text
        FROM documents
        ORDER BY embedding <=> '{vector}'::vector
        LIMIT 5
    """

    cur.execute(query)

    results = cur.fetchall()

    release_connection(conn)

    return [r[0] for r in results]

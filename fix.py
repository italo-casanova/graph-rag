import psycopg2
import os

DB_HOST = os.getenv(
    "RDSHOST",
    "postgres-instance-1.chamsaceyyb6.us-west-2.rds.amazonaws.com"
)

DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mastermaster")
DB_PORT = os.getenv("DB_PORT", "5432")


def connect():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


def ensure_doc_id_column(cur):
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='documents'
        AND column_name='doc_id'
        """
    )

    if cur.fetchone() is None:
        print("Adding doc_id column...")
        cur.execute(
            """
            ALTER TABLE documents
            ADD COLUMN doc_id TEXT
            """
        )
    else:
        print("doc_id column already exists")


def ensure_doc_id_index(cur):
    cur.execute(
        """
        SELECT indexname
        FROM pg_indexes
        WHERE tablename='documents'
        AND indexname='documents_doc_id_idx'
        """
    )

    if cur.fetchone() is None:
        print("Creating doc_id index...")
        cur.execute(
            """
            CREATE INDEX documents_doc_id_idx
            ON documents(doc_id)
            """
        )
    else:
        print("doc_id index already exists")


def ensure_vector_index(cur):
    cur.execute(
        """
        SELECT indexname
        FROM pg_indexes
        WHERE tablename='documents'
        AND indexname='documents_embedding_idx'
        """
    )

    if cur.fetchone() is None:
        print("Creating pgvector index...")
        cur.execute(
            """
            CREATE INDEX documents_embedding_idx
            ON documents
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100)
            """
        )
    else:
        print("vector index already exists")


def main():

    conn = connect()
    cur = conn.cursor()

    print("Fixing PostgreSQL schema...")

    ensure_doc_id_column(cur)
    ensure_doc_id_index(cur)
    ensure_vector_index(cur)

    conn.commit()

    cur.close()
    conn.close()

    print("Schema ready")


if __name__ == "__main__":
    main()
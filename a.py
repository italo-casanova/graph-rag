import logging

from graph.graph_client import submit_query
from db.postgres import get_connection, release_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cleanup")


# -----------------------------
# NEPTUNE CLEANUP
# -----------------------------


def clean_neptune():
    logger.info("🧹 Cleaning Neptune graph...")

    try:
        submit_query("g.V().drop()")
        logger.info("✅ Neptune graph cleaned")

    except Exception as e:
        logger.error(f"❌ Failed to clean Neptune: {e}")


# -----------------------------
# POSTGRES CLEANUP
# -----------------------------


def clean_postgres():
    logger.info("🧹 Cleaning PostgreSQL...")

    conn = None

    try:
        conn = get_connection()
        cur = conn.cursor()

        # limpia tabla principal
        cur.execute("DELETE FROM documents;")

        # opcional: reset de secuencias (si tienes SERIAL)
        cur.execute("""
        DO $$
        DECLARE
            r RECORD;
        BEGIN
            FOR r IN (
                SELECT sequence_name
                FROM information_schema.sequences
                WHERE sequence_schema = 'public'
            )
            LOOP
                EXECUTE 'ALTER SEQUENCE ' || r.sequence_name || ' RESTART WITH 1';
            END LOOP;
        END $$;
        """)

        conn.commit()

        logger.info("✅ PostgreSQL cleaned")

    except Exception as e:
        logger.error(f"❌ Failed to clean PostgreSQL: {e}")

        if conn:
            conn.rollback()

    finally:
        if conn:
            release_connection(conn)


# -----------------------------
# MAIN
# -----------------------------


def main():
    print("\n⚠️  WARNING: This will DELETE ALL DATA from:")
    print("   - Neptune (graph)")
    print("   - PostgreSQL (documents table)\n")

    confirm = input("Type 'yes' to continue: ")

    if confirm.lower() != "yes":
        print("❌ Aborted")
        return

    clean_neptune()
    clean_postgres()

    logger.info("🎯 Cleanup completed successfully")


if __name__ == "__main__":
    main()

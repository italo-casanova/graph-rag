from psycopg2 import pool
from config import RDS_HOST, RDS_DB, RDS_USER, RDS_PASSWORD, RDS_PORT

connection_pool = pool.SimpleConnectionPool(
    1,
    10,
    host=RDS_HOST,
    database=RDS_DB,
    user=RDS_USER,
    password=RDS_PASSWORD,
    port=RDS_PORT,
)


def get_connection():
    return connection_pool.getconn()


def release_connection(conn):
    connection_pool.putconn(conn)

import logging
import time

from gremlin_python.driver import client
from gremlin_python.driver.serializer import GraphSONSerializersV2d0

from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.session import get_session

from config import NEPTUNE_HOST, NEPTUNE_PORT, AWS_REGION

logger = logging.getLogger("neptune")

MAX_RETRIES = 5

_gremlin_client = None


def _signed_headers():
    session = get_session()
    credentials = session.get_credentials()

    request = AWSRequest(
        method="GET", url=f"https://{NEPTUNE_HOST}:{NEPTUNE_PORT}/gremlin"
    )

    SigV4Auth(credentials, "neptune-db", AWS_REGION).add_auth(request)

    return dict(request.headers)


def _create_client():
    endpoint = f"wss://{NEPTUNE_HOST}:{NEPTUNE_PORT}/gremlin"

    return client.Client(
        endpoint,
        "g",
        headers=_signed_headers(),
        message_serializer=GraphSONSerializersV2d0(),
    )


def get_client():
    global _gremlin_client

    if _gremlin_client is None:
        _gremlin_client = _create_client()

    return _gremlin_client


def _reset_client():
    global _gremlin_client

    try:
        if _gremlin_client:
            _gremlin_client.close()
    except:
        pass

    _gremlin_client = None


def submit_query(query):

    for attempt in range(MAX_RETRIES):

        try:
            logger.info(f"Executing Gremlin query:\n{query}")

            g = get_client()

            result = g.submit(query).all().result()

            return result

        except Exception as e:

            error = str(e)

            # 🔁 retry conocidos
            if any(
                x in error
                for x in [
                    "ConcurrentModificationException",
                    "ReadOnlyViolationException",
                    "TimeoutException",
                ]
            ):
                wait = 0.5 * (attempt + 1)
                logger.warning(f"Retryable error, retrying in {wait}s...")
                time.sleep(wait)
                continue

            # 🔥 errores de conexión → recrear cliente
            if any(
                x in error
                for x in [
                    "Connection refused",
                    "WebSocket",
                    "closed",
                    "Failed to write",
                ]
            ):
                logger.warning("Connection issue → resetting client")
                _reset_client()
                time.sleep(1)
                continue

            # ❌ error real → no retry
            logger.error(f"Gremlin query failed: {error}")
            raise e

    raise Exception("Max retries exceeded for Gremlin query")

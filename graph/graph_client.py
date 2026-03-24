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


def submit_query(query):

    for attempt in range(MAX_RETRIES):

        try:

            logger.info("Executing Gremlin query")

            g = _create_client()

            result = g.submit(query).all().result()

            g.close()

            return result

        except Exception as e:

            if "ConcurrentModificationException" in str(e):

                wait = 0.5 * (attempt + 1)

                logger.warning(
                    f"Concurrent modification detected, retrying in {wait}s..."
                )

                time.sleep(wait)

                continue

            raise e

    raise Exception("Max retries exceeded for Gremlin query")


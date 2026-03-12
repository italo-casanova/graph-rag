# import logging
# import time

# from gremlin_python.driver import client
# from gremlin_python.driver.serializer import GraphSONSerializersV2d0

# # from botocore.auth import SigV4Auth
# # from botocore.awsrequest import AWSRequest
# # from botocore.session import get_session

# from config import NEPTUNE_HOST, NEPTUNE_PORT


# logger = logging.getLogger("neptune")

# MAX_RETRIES = 5


# # def _signed_headers():

# #     session = get_session()
# #     credentials = session.get_credentials()

# #     request = AWSRequest(
# #         method="GET",
# #         url=f"https://{NEPTUNE_HOST}:{NEPTUNE_PORT}/gremlin"
# #     )

# #     SigV4Auth(credentials, "neptune-db", AWS_REGION).add_auth(request)

# #     return dict(request.headers)


# def _create_client():

#     endpoint = f"wss://{NEPTUNE_HOST}:{NEPTUNE_PORT}/gremlin"

#     return client.Client(
#         endpoint,
#         "g",
#         # headers=_signed_headers(),
#         message_serializer=GraphSONSerializersV2d0(),
#     )


# def submit_query(query):

#     for attempt in range(MAX_RETRIES):

#         try:

#             logger.info("Executing Gremlin query")

#             g = _create_client()

#             result = g.submit(query).all().result()

#             g.close()

#             return result

#         except Exception as e:

#             if "ConcurrentModificationException" in str(e):

#                 wait = 0.5 * (attempt + 1)

#                 logger.warning(
#                     f"Concurrent modification detected, retrying in {wait}s..."
#                 )

#                 time.sleep(wait)

#                 continue

#             raise e

#     raise Exception("Max retries exceeded for Gremlin query")


import logging
import time
import threading

from gremlin_python.driver import client
from gremlin_python.driver.serializer import GraphSONSerializersV3d0

from config import GREMLIN_ENDPOINT

logger = logging.getLogger("graph")

MAX_RETRIES = 5

_client = None
_lock = threading.Lock()


def _get_client():
    """
    Create persistent Gremlin client
    """

    global _client

    if _client is None:

        logger.info(f"Connecting to Gremlin server {GREMLIN_ENDPOINT}")

        _client = client.Client(
            GREMLIN_ENDPOINT,
            "g",
            message_serializer=GraphSONSerializersV3d0(),
        )

    return _client


def submit_query(query):

    for attempt in range(MAX_RETRIES):

        try:

            g = _get_client()

            with _lock:

                result = g.submit(query).all().result()

            return result

        except Exception as e:

            if "ConcurrentModificationException" in str(e):

                wait = 0.5 * (attempt + 1)

                logger.warning(
                    f"Concurrent modification detected, retrying in {wait}s..."
                )

                time.sleep(wait)

                continue

            logger.error("Gremlin query failed")
            logger.error(e)

            raise e

    raise Exception("Max retries exceeded")


def close_client():

    global _client

    if _client:

        logger.info("Closing Gremlin client")

        _client.close()

        _client = None
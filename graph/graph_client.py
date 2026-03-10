from gremlin_python.driver import client
from gremlin_python.driver.serializer import GraphSONSerializersV2d0
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.session import get_session
from config import NEPTUNE_HOST, NEPTUNE_PORT, AWS_REGION
from logger import get_logger

logger = get_logger("neptune")

session = get_session()
credentials = session.get_credentials()

SERVICE = "neptune-db"


def signed_headers():

    request = AWSRequest(
        method="GET", url=f"https://{NEPTUNE_HOST}:{NEPTUNE_PORT}/gremlin"
    )

    SigV4Auth(credentials, SERVICE, AWS_REGION).add_auth(request)

    return dict(request.headers)


def get_client():

    return client.Client(
        f"wss://{NEPTUNE_HOST}:{NEPTUNE_PORT}/gremlin",
        "g",
        headers=signed_headers(),
        message_serializer=GraphSONSerializersV2d0(),
    )


def submit_query(query):

    logger.info("Executing Gremlin query")

    g = get_client()

    try:
        result = g.submit(query).all().result()
        return result
    finally:
        g.close()

import os

AWS_REGION = "us-west-2"

BEDROCK_MODEL = "us.amazon.nova-pro-v1:0"
EMBED_MODEL = "amazon.titan-embed-text-v1"

RDS_HOST = os.getenv(
    "RDSHOST", "postgres-instance-1.chamsaceyyb6.us-west-2.rds.amazonaws.com"
)

RDS_DB = "postgres"
RDS_USER = "postgres"
RDS_PASSWORD = "mastermaster"
RDS_PORT = 5432

NEPTUNE_HOST = (
    "db-neptune-1-legal-instance-1.chamsaceyyb6.us-west-2.neptune.amazonaws.com"
)
NEPTUNE_PORT = 8182

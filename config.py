import os

AWS_REGION = "us-east-1"

BEDROCK_MODEL = "us.amazon.nova-pro-v1:0"
EMBED_MODEL = "amazon.titan-embed-text-v1"

RDS_HOST = os.getenv("RDSHOST", "database-1.cecua5pujewa.us-east-1.rds.amazonaws.com")

RDS_DB = "postgres"
RDS_USER = "postgres"
RDS_PASSWORD = "mastermaster"
RDS_PORT = 5432

NEPTUNE_HOST = "db-neptune-1-instance-1.cecua5pujewa.us-east-1.neptune.amazonaws.com"
NEPTUNE_PORT = 8182

# # postgres
# RDS_HOST = "localhost"
# RDS_DB = "rag"
# RDS_USER = "postgres"
# RDS_PASSWORD = "postgres"
# RDS_PORT = 5432
#
# # gremlin
# GREMLIN_ENDPOINT = "ws://localhost:8182/gremlin"
#
# # ollama
# OLLAMA_URL = "http://localhost:11434"
# LLM_MODEL = "llama3"
# EMBED_MODEL = "nomic-embed-text"

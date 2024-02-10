# create a cosmosdb 

import os
import time
from dotenv import load_dotenv
from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from openai import AzureOpenAI
    


# Load the .env file
load_dotenv()

# Get the environment variables
COSMOSDB_URI = os.getenv('COSMOSDB_URI')
COSMOSDB_KEY = os.getenv('COSMOSDB_KEY')
COSMOSDB_DBNAME = os.getenv('COSMOSDB_DBNAME')
#
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

# Initialize Cosmos Client
client = CosmosClient(COSMOSDB_URI, credential=COSMOSDB_KEY)
print(f"Connected to CosmosDB: {COSMOSDB_URI}")

# connecto to container "kb_store"
collection_name = "kb_store"
database = client.get_database_client(COSMOSDB_DBNAME)
container = database.get_container_client(collection_name)
print(f"Connected to CosmosDB container: {collection_name}")

# Initialize Azure OpenAI client
openai_client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,  
    api_version="2023-12-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT)
print(f"Connected to Azure OpenAI: {AZURE_OPENAI_ENDPOINT}")

# for each document in the container, generate embeddings and update the document
query = "SELECT * FROM c"
for doc in container.query_items(query, enable_cross_partition_query=True):
    print(f"Generating embeddings for document: {doc['id']}")
    embeddings = openai_client.generate_embeddings(doc["text"])
    doc["embeddings"] = embeddings
    container.upsert_item(doc)
    print(f"Embeddings generated and updated for document: {doc['id']}")
    time.sleep(1)  # sleep for 1 second to avoid rate limiting
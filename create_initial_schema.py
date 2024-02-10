# create a cosmosdb 

import os
from dotenv import load_dotenv
from azure.core.exceptions import AzureError
from azure.cosmos import CosmosClient, PartitionKey, exceptions


# Load the .env file
load_dotenv()

# Get the environment variables
COSMOSDB_URI = os.getenv('COSMOSDB_URI')
COSMOSDB_KEY = os.getenv('COSMOSDB_KEY')
COSMOSDB_DBNAME = os.getenv('COSMOSDB_DBNAME')

# Initialize Cosmos Client
client = CosmosClient(COSMOSDB_URI, credential=COSMOSDB_KEY)
print(f"Connected to CosmosDB: {COSMOSDB_URI}")

collections = {
    "prompt_store": "/prompt_id",
    "kb_store": "/source_id",
    "action_log": "/session_id",
    "session_log": "/session_id",
    # Add more collections as needed
}

# Create a database if it doesn't exist
try:
    print(f"Creating database '{COSMOSDB_DBNAME}'...")
    database = client.create_database(COSMOSDB_DBNAME)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(COSMOSDB_DBNAME)
    print(f"Database '{COSMOSDB_DBNAME}' already exists.")

# Create a container if it doesn't exist
# Loop over the collections
for collection_name, partition_key in collections.items():
    # Create a container if it doesn't exist
    try:
        container = database.create_container(id=collection_name, partition_key=PartitionKey(path=partition_key))
        print(f"Container '{collection_name}' created.")
    except exceptions.CosmosResourceExistsError:
        container = database.get_container_client(collection_name)
        print(f"Container '{collection_name}' already exists.")

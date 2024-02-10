# create a cosmosdb 

import os
import time
from dotenv import load_dotenv
from azure.core.exceptions import AzureError
from gremlin_python.driver import client, serializer

# Load the .env file
load_dotenv()

# Get the environment variables
COSMOSDB_GREMLIN_URI = os.getenv('COSMOSDB_GREMLIN_URI')
COSMOSDB_KEY = os.getenv('COSMOSDB_KEY')
COSMOSDB_DBNAME = os.getenv('COSMOSDB_DBNAME')

# dictionary of dictionary made for synthetic_data files;
# keys are random source_id and values are a dict with category_name and file_path
data = {
    "1": {
        "category_name": "airline",
        "id_col_index": 0,
        "file_path": "synthetic_data/further_modified_synthetic_airline_data.csv"
    }
    #,
    # "2": {
    #     "category_name": "communication",
    #     "id_col_index": "0",
    #     "file_path": "synthetic_data/further_modified_synthetic_communication_data.csv"
    # }
    #,
    # "3": {
    #     "category_name": "manufacturing",
    #     "id_col_index": "0",
    #     "file_path": "synthetic_data/further_modified_synthetic_manufacturing_data.csv"
    # },
}

# Initialize the Gremlin client
gremlin_client = client.Client(f"{COSMOSDB_GREMLIN_URI}", 
                               traversal_source="g",
                               username=f"/dbs/{COSMOSDB_DBNAME}/colls/kb_store",
                               password=f"{COSMOSDB_KEY}",
                               message_serializer=serializer.GraphSONSerializersV2d0())

# source_id is the partition key
for source_id, value in data.items():
    category_name = value["category_name"]
    file_path = value["file_path"]
    print(f"Inserting {file_path} into CosmosDB")

    # Load the data from the csv file
    insert_count = 0
    with open(file_path, "r") as file:
        lines = file.readlines()
        headers = lines[0].strip().split(",")
        for line in lines[1:]:
            data = line.strip().split(",")
            item_id = data[0]
            data = {headers[i]: data[i] for i in range(len(headers))}
            data["source_id"] = source_id            
            data["category_name"] = category_name
            data["item_id"] = item_id
            data["vector"] = ""

            # convert the data to a vertex, include all the dynamic properties
            vertice_name = f"{data['source_id']}_{data['category_name']}_{data['item_id']}"
            
            # for each column in the data, add a property to the vertex
            vertice_properties = ""
            for key, value in data.items():
                if key not in ["vector"]:
                    vertice_properties += f".property('{key}', '{value}')"
            
            query = f"g.addV('{vertice_name}'){vertice_properties}"
            
            callback = gremlin_client.submitAsync(query)
            if callback.result() is not None:
                print("Inserted vertice {0}".format(vertice_name))
            else:
                print("Something went wrong with the query")
            
            time.sleep(0.5)  # Add a delay of 1 second between each operation
        
                        
            # stop the loop after 25 inserts
            insert_count += 1
            # if insert_count == 5:
            #     break
            
print("Data inserted into CosmosDB")
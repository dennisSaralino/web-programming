import json
# Creating a Mongita database with movie information
from mongita import MongitaClientDisk

quotes_data = [
    {"text": "Meow", "author": "Torch"},
    {"text": "Live long and prosper", "author": "Spock"},
]

# open a mongita client connection
client = MongitaClientDisk()

# open a quote database
quotes_db = client.quotes_db

# open a squotes collection
quotes_collection = quotes_db.quotes_collection

# empty the collection
quotes_collection.delete_many({})

# put the quotes in the database
quotes_collection.insert_many(quotes_data)

# make sure the quotes are there
print(quotes_collection.count_documents({}))
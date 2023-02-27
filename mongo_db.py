import pymongo

# Set up the connection to the MongoDB server
client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")

# Select the database to use
db = client["vacancy_manager"]

# Select the collection to use
collection = db["contacts"]

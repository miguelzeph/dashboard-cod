from mongomock import MongoClient

client = MongoClient()
db = client["dataScience"]
collection = db["pubmedArticles_synonyms_blacklist"]

doc1 = {"synonym": "LU13"}

doc2 = {"synonyms": "CNX-234"}

collection.insert_many([doc1, doc2])

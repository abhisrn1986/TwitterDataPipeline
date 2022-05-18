import pymongo

def connect_to_mongodb():
    # Establish a connection to the MongoDB server
    client = pymongo.MongoClient(host="mongodb", port=27017, replicaset='dbrs')

    # Select the database you want to use withing the MongoDB server
    return client.twitter

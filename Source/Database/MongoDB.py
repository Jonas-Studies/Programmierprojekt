from pymongo import MongoClient

MONGODB_HOSTNAME = "localhost"
MONGODB_PORT = 27017

DATABASE_NAME = "designerdrugdatabase"

class Substances:
    COLLECTION_NAME = "substances"

    def __init__(self) -> None:
        self.connection = MongoClient(MONGODB_HOSTNAME, MONGODB_PORT)
        self.collection = self.connection[DATABASE_NAME][self.COLLECTION_NAME]

        return
    
    def __del__(self) -> None:
        self.connection.close()

        return

    def insert_substance (self, substance) -> None:
        self.collection.insert_one(substance)

        return
    
    def update_substance_by_id(self, id, substance) -> None:
        searchCriterias = {
            "_id": id
        }

        self.collection.replace_one(searchCriterias, substance)

        return
    
    def get_substances (self, searchCriteria) -> list:
        substances = self.collection.find(searchCriteria)

        result = []

        for substance in substances:
            result.append(substance)

        return result
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

    def InsertSubstance (self, substance) -> None:
        self.collection.insert_one(substance)

        return
    
    def GetSubstances (self, searchCriteria) -> list:
        substances = self.collection.find(searchCriteria)

        result = []

        for substance in substances:
            result.append(substance)

        return result
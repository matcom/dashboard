import os

import pymongo
from models.custom_model import collection_names

ROOT_USER = os.environ["DB_ROOT_USER"]
ROOT_PASS = os.environ["DB_ROOT_PASS"]
DATABSE_NAME = "dashboardDB"

client = pymongo.MongoClient(f"mongodb://{ROOT_USER}:{ROOT_PASS}@mongo:27017/")
db = client[DATABSE_NAME]


def migrate_collections():
    for model_class, name in collection_names.items():
        print("Updating", name)
        coll = db[name]
        coll.drop()
        for item in model_class.all():
            dict_item = item.encode()
            coll.update_one(
                {"uuid": dict_item["uuid"]}, {"$set": dict_item}, upsert=True
            )


if __name__ == "__main__":
    migrate_collections()

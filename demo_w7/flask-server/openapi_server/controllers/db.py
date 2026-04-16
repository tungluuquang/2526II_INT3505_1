import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self):
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.client = MongoClient(uri)
        self.db = self.client[os.getenv("DB_NAME", "ecommerce_db")]

    def get_collection(self, name):
        return self.db[name]

db_instance = MongoDB()

def get_db():
    return db_instance.db

def init_db():
    db = get_db()
    db.categories.create_index("slug", unique=True)

    db.products.create_index("sku", unique=True)

    print("Đã kết nối MongoDB và khởi tạo thành công các Unique Index!")
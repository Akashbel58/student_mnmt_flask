
#  set up MongoDB conection

import pymongo
from config import MONGO_URL,DB_NAME

def db_connection():

    mongo_client    = pymongo.MongoClient(MONGO_URL)
    student_db      = mongo_client[DB_NAME]
    student_collection = student_db['student_data']

    print(student_collection)
    return student_collection
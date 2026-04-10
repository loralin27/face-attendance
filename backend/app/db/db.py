from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')  # check connection

    db = client["face_attendance"]
    attendance_collection = db["attendance"]

    print(" MongoDB Connected Successfully")

except Exception as e:
    print(" MongoDB Error:", e)
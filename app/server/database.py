import os
# import motor.motor_asyncio
import pymongo
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()


s = MongoClient(os.getenv("MONGODBURI"),
                tlsCAFile=certifi.where())
MONGO_DETAILS = os.getenv("MONGODBURI")
# MONGO_DETAILS = "mongodb+srv://mongo-practice:fastapi@cluster0.3enmm.mongodb.net/test"
# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = s.users
user_collection = database.get_collection("users_collection")


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "course_of_study": user["course_of_study"],
        "year": user["year"],
        "GPA": user["gpa"],
    }

# Retrieve all users present in the database


async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the database
def add_user(user_data: dict) -> dict:
    import pdb
    # pdb.set_trace()
    user = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Retrieve a user with a matching ID
def retrieve_user(id: str) -> dict:
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


# Update a user with a matching ID
async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a user from the database
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True

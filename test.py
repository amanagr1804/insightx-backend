from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI

# Connect to the MongoDB/DocumentDB
client = MongoClient(MONGO_URI)
db = client['insightx']
reports_collection = db['reports']

# You can assign a default user_id or create a mapping
DEFAULT_USER_ID = "6716798b5b66ae3dd431cbec"  # Replace with a valid user_id (string or ObjectId)

# Find all reports where 'user_id' is missing or set to None
reports_without_user_id = reports_collection.find({"user_id": {"$exists": False}})

# Loop over each report and update it with the user_id
for report in reports_without_user_id:
    report_id = report['_id']
    # Update the report with the DEFAULT_USER_ID (you can change logic here if needed)
    result = reports_collection.update_one(
        {"_id": report_id},  # Filter by report ID
        {"$set": {"user_id": DEFAULT_USER_ID}}  # Add or update the 'user_id' field
    )
    if result.modified_count > 0:
        print(f"Updated report with _id: {report_id}")
    else:
        print(f"Failed to update report with _id: {report_id}")

print("User ID update complete.")

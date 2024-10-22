from fastapi import APIRouter, Depends, HTTPException
from app.services.auth_service import AuthService
from pymongo import MongoClient
from config import MONGO_URI
from bson import ObjectId  # Import ObjectId to handle MongoDB object IDs


auth_service = AuthService()
client = MongoClient(MONGO_URI)
db = client['insightx']

router = APIRouter()
# Helper function to convert MongoDB ObjectId to string
def convert_objectid_to_str(report):
    if '_id' in report:
        report['_id'] = str(report['_id'])  # Convert ObjectId to string
    if 'user_id' in report and isinstance(report['user_id'], ObjectId):
        report['user_id'] = str(report['user_id'])  # Convert user_id ObjectId to string
    return report

# Protected route - fetch all reports (requires Bearer token)
@router.get("/reports")
def get_reports(current_user: dict = Depends(auth_service.get_current_user)):
    user_id = current_user['user_id']
    
    # Fetch all reports belonging to the user
    reports = db['reports'].find({"user_id": user_id})  # Use ObjectId to query by user_id
    
    # Convert ObjectId in reports to string before returning the response
    reports_list = [convert_objectid_to_str(report) for report in reports]
    
    return {"reports": reports_list}

# Protected route - fetch a specific report (requires Bearer token)
@router.get("/report/{report_id}")
def fetch_report(report_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    print("user_id",current_user['user_id'])

    report = db['reports'].find_one({"_id": ObjectId(report_id), "user_id": current_user['user_id']})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"report": convert_objectid_to_str(report)}

# Protected route - create a report (requires Bearer token)
@router.post("/report")
def save_report(report_data: dict, current_user: dict = Depends(auth_service.get_current_user)):
    report_data['user_id'] = current_user['user_id']
    db['reports'].insert_one(report_data)
    return {"message": "Report saved"}

# Protected route - update a report (requires Bearer token)
@router.put("/report/{report_id}")
def edit_report(report_id: str, report_data: dict, current_user: dict = Depends(auth_service.get_current_user)):
    result = db['reports'].update_one({"_id": report_id, "user_id": current_user['user_id']}, {"$set": report_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Report not found or not owned by user")
    return {"message": "Report updated"}

# Protected route - delete a report (requires Bearer token)
@router.delete("/report/{report_id}")
def delete_report(report_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    result = db['reports'].delete_one({"_id": report_id, "user_id": current_user['user_id']})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Report not found or not owned by user")
    return {"message": "Report deleted"}
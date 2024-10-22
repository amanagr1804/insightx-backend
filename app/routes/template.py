from fastapi import APIRouter, Depends, HTTPException
from app.services.auth_service import AuthService
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId to handle MongoDB object IDs
from config import MONGO_URI


auth_service = AuthService()
client = MongoClient(MONGO_URI)
db = client['insightx']



router = APIRouter()


def convert_objectid_to_str(report):
    if '_id' in report:
        report['_id'] = str(report['_id'])  # Convert ObjectId to string
    if 'user_id' in report and isinstance(report['user_id'], ObjectId):
        report['user_id'] = str(report['user_id'])  # Convert user_id ObjectId to string
    return report

@router.get("/templates")
def get_templates(current_user: dict = Depends(auth_service.get_current_user)):
    templates = db['templates'].find({"user_id": current_user['user_id']})
    templates_list = [convert_objectid_to_str(report) for report in templates]
    return {"templates": list(templates_list)}

@router.get("/template/{template_id}")
def fetch_template(template_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    template = db['templates'].find_one({"_id": ObjectId(template_id), "user_id": current_user['user_id']})
    template = convert_objectid_to_str(template)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"template": template}

@router.post("/template")
def save_template(template_data: dict, current_user: dict = Depends(auth_service.get_current_user)):
    template_data['user_id'] = current_user['user_id']
    db['templates'].insert_one(template_data)
    return {"message": "Template saved"}

@router.put("/template/{template_id}")
def edit_template(template_id: str, template_data: dict, current_user: dict = Depends(auth_service.get_current_user)):
    result = db['templates'].update_one({"_id": ObjectId(template_id), "user_id": current_user['user_id']}, {"$set": template_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Template not found or not owned by user")
    return {"message": "Template updated"}

@router.delete("/template/{template_id}")
def delete_template(template_id: str, current_user: dict = Depends(auth_service.get_current_user)):
    result = db['templates'].delete_one({"_id": ObjectId(template_id), "user_id": current_user['user_id']})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Template not found or not owned by user")
    return {"message": "Template deleted"}

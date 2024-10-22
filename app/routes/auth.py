from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.auth_service import AuthService
from pymongo import MongoClient
from config import MONGO_URI
from app.models import UserSignup, UserLogin

auth_service = AuthService()
client = MongoClient(MONGO_URI)
db = client['insightx']
router = APIRouter()

# Public route - signup
@router.post("/signup")
def signup(user: UserSignup):
    hashed_password = auth_service.hash_password(user.password)
    existing_user = db['users'].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    new_user = {"email": user.email, "hashed_password": hashed_password}
    db['users'].insert_one(new_user)
    token = auth_service.create_jwt(str(new_user['_id']))
    return {"token": token}

# Public route - login
@router.post("/login")
def login(user: UserLogin):
    existing_user = db['users'].find_one({"email": user.email})
    if not existing_user or not auth_service.verify_password(user.password, existing_user['hashed_password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth_service.create_jwt(str(existing_user['_id']))
    return {"token": token}

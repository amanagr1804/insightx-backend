import bcrypt
import jwt
import datetime
from google.oauth2 import id_token
from google.auth.transport import requests
from config import JWT_SECRET, GOOGLE_CLIENT_ID
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class AuthService:
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    def create_jwt(self, user_id):
        return jwt.encode({
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, JWT_SECRET, algorithm="HS256")

    def verify_jwt(self, token: str):
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        token = credentials.credentials  # Extract token from "Bearer <token>"
        decoded_token = self.verify_jwt(token)
        if decoded_token is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return decoded_token

from fastapi import Request, HTTPException
from app.services.auth_service import AuthService

auth_service = AuthService()

async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token:
        token = token.split("Bearer ")[1]
        user = auth_service.verify_jwt(token)
        if user:
            request.state.user = user
            return await call_next(request)
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")

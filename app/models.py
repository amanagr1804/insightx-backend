from pydantic import BaseModel, EmailStr

# Model for user signup
class UserSignup(BaseModel):
    email: EmailStr
    password: str

# Model for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
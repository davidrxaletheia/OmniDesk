from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.security import create_access_token, verify_password
from ..repos.app_user_repo import AppUserRepo

class LoginRequest(BaseModel):
    username: str
    password: str

router = APIRouter()

@router.post("/login")
def login(body: LoginRequest):
    user = AppUserRepo().get_by_username(body.username)
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"username": user.username, "user_id": user.user_id})
    return {"access_token": token, "token_type": "bearer", "user": user.dict(exclude={"password_hash"})}
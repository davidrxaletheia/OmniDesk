from fastapi import Depends, Header, HTTPException
from .security import decode_token
from ..repos.app_user_repo import AppUserRepo  # adapter/wrapper
from ..repos.client_repo import ClientRepo

def get_bearer_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing Authorization")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(401, "Invalid Authorization header")
    return parts[1]

def get_current_user(token: str = Depends(get_bearer_token)):
    payload = decode_token(token)
    sub = payload.get("sub", {})
    username = sub.get("username")
    if not username:
        raise HTTPException(401, "Invalid token")
    user = AppUserRepo().get_by_username(username)
    if not user:
        raise HTTPException(401, "User not found")
    return user


def get_current_client(token: str = Depends(get_bearer_token)):
    payload = decode_token(token)
    sub = payload.get("sub", {})
    client_id = sub.get("client_id")
    if not client_id:
        raise HTTPException(401, "Invalid client token")
    client = ClientRepo().get(client_id)
    if not client:
        raise HTTPException(401, "Client not found")
    return client


def require_admin(current_user=Depends(get_current_user)):
    # current_user is a Pydantic model or fallback with attribute `role`
    role = getattr(current_user, 'role', None)
    if role != 'admin':
        raise HTTPException(403, "Admin privileges required")
    return current_user


def require_employee_or_admin(current_user=Depends(get_current_user)):
    role = getattr(current_user, 'role', None)
    if role not in ('admin', 'empleado'):
        raise HTTPException(403, "Employee or admin privileges required")
    return current_user


def require_client(current_client=Depends(get_current_client)):
    return current_client
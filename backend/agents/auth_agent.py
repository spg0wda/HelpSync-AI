import os
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from data.postgres_store import (
    create_user_account,
    get_user_account_by_username
)


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def register_user(
    username: str,
    email: str | None,
    full_name: str | None,
    password: str
) -> dict:
    if len(username.strip()) < 3:
        return {
            "registered": False,
            "message": "Username must be at least 3 characters."
        }

    if len(password) < 6:
        return {
            "registered": False,
            "message": "Password must be at least 6 characters."
        }

    hashed_password = get_password_hash(password)

    result = create_user_account(
        username=username.strip(),
        email=email.strip() if email else None,
        full_name=full_name.strip() if full_name else None,
        hashed_password=hashed_password
    )

    return {
        "registered": result.get("created", False),
        "message": result.get("message"),
        "user": result.get("user")
    }


def authenticate_user(username: str, password: str) -> dict | None:
    user = get_user_account_by_username(username)

    if not user:
        return None

    if not user.get("is_active"):
        return None

    if not verify_password(password, user.get("hashed_password")):
        return None

    return user


def login_user(username: str, password: str) -> dict:
    user = authenticate_user(username, password)

    if not user:
        return {
            "logged_in": False,
            "message": "Invalid username or password."
        }

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "sub": user["username"],
            "role": user["role"]
        },
        expires_delta=access_token_expires
    )

    safe_user = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
        "is_active": user["is_active"]
    }

    return {
        "logged_in": True,
        "message": "Login successful.",
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
        "user": safe_user
    }


def get_current_active_user(token: str = Depends(oauth2_scheme)) -> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate authentication token.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    user = get_user_account_by_username(username)

    if user is None:
        raise credentials_exception

    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive."
        )

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"],
        "is_active": user["is_active"]
    }
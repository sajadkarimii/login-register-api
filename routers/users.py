from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from oprations.users import UsersOpration
from db.engine import get_db
from schema._input import RegisterInput, LoginInput
from schema.output import UserOutput
from utils.secrets import password_manager
from utils.jwt import JWTHandler
from schema.jwt import JWTPayload

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserOutput)
@limiter.limit("10/minute")
async def register(
        request: Request,
        db_session: Annotated[AsyncSession, Depends(get_db)],
        data: RegisterInput = Body(),
):
    password = password_manager.hash(data.password)
    user = await UsersOpration(db_session).create(
        username=data.username,
        password=password,
        fullname=data.fullname,
        phone=data.phone,
        email=data.email,
        address=data.address
    )
    return user


@router.post("/login")
@limiter.limit("5/minute")
async def login(
        request: Request,
        db_session: Annotated[AsyncSession, Depends(get_db)],
        data: LoginInput = Body(),
):
    token = await UsersOpration(db_session).login(data.username, data.password)
    return token


@router.get("/{username}/", response_model=UserOutput)
@limiter.limit("20/minute")
async def get_user_profile(
        request: Request,
        db_session: Annotated[AsyncSession, Depends(get_db)],
        username: str,
        token_data: JWTPayload = Depends(JWTHandler.verify_token),
):
    if token_data.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied - You can only view your own profile"
        )

    user_profile = await UsersOpration(db_session).get_by_username(username)
    return user_profile


@router.delete("/{username}/")
@limiter.limit("5/minute")
async def delete_user(
        request: Request,
        db_session: Annotated[AsyncSession, Depends(get_db)],
        username: str,
        token_data: JWTPayload = Depends(JWTHandler.verify_token),
):
    if token_data.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied - You can only delete your own account"
        )

    await UsersOpration(db_session).delete_account(username)
    return {"message": "User account deleted successfully"}
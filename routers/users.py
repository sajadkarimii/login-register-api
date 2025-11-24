from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from oprations.users import UsersOpration
from db.engine import get_db
from schema._input import RegisterInput, DeleteUserInput, LoginInput
from schema.output import UserOutput
from utils.secrets import password_manager

router = APIRouter()

@router.post("/register", response_model=UserOutput)
async def register(
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
async def login(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: LoginInput = Body(),
):
    token = await UsersOpration(db_session).login(data.username, data.password)
    return token

@router.get("/{username}/", response_model=UserOutput)
async def get_user_profile(db_session: Annotated[AsyncSession, Depends(get_db)],username: str,):
    user_profile = await UsersOpration(db_session).get_by_username(username)
    return user_profile

@router.delete("/{username}/")
async def delete_user(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: DeleteUserInput = Body(),
):
    await UsersOpration(db_session).delete_account(data.username, data.password)


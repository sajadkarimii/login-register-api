from sqlalchemy.ext.asyncio import AsyncSession
from db import User
import exceptions
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from utils.secrets import password_manager
from utils.jwt import JWTHandler
from schema.jwt import JWTResponsePayload


class UsersOpration:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, username: str, password: str, fullname: str, phone: str, email: str, address: str) -> User:
        user = User(username=username,password=password,fullname=fullname,phone=phone,email=email,address=address)
        async with self.db_session as session:
            try:
                session.add(user)
                await session.commit()
            except IntegrityError:
                raise exceptions.UserAlreadyExist

        return user

    async def get_by_username(self, username: str) -> User:
        query = sa.select(User).where(User.username == username)
        async with self.db_session as session:
            user = await session.scalar(query)
            if user is None:
                raise exceptions.UserNotFound
            return user

    async def delete_account(self, username: str) -> None:
        query = sa.delete(User).where(User.username == username)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def login(self, username: str, password: str) -> JWTResponsePayload:
        query = sa.select(User).where(User.username == username)
        async with self.db_session as session:
            user = await session.scalar(query)
            if user is None:
                raise exceptions.UsernameOrPasswordIncorrect
        if not password_manager.verify(password, user.password):
            raise exceptions.UsernameOrPasswordIncorrect
        return JWTHandler.generate(username)
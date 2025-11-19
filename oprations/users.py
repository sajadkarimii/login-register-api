from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from db import User
import sqlalchemy as sa

class UsersOpration:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, username: str, password: str, fullname: str, phone: str, email: str, address: str) -> User:
        user = User(username=username,password=password,fullname=fullname,phone=phone,email=email,address=address)
        async with self.db_session as session:
            session.add(user)
            await session.commit()

        return user

    async def get_by_username(self, username: str) -> User:
        query = sa.select(User).where(User.username == username)
        async with self.db_session as session:
            user = await session.scalar(query)
            if user is None:
                raise ValidationError("User not found")
            return user

    async def delete_account(self, username: str, password: str) -> None:
        query = sa.delete(User).where(User.username == username, User.password == password)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
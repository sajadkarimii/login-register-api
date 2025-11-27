from sqlalchemy.ext.asyncio import AsyncSession
from db import User
import exceptions
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import logging

from utils.secrets import password_manager
from utils.jwt import JWTHandler
from schema.jwt import JWTResponsePayload

logging.basicConfig(level=logging.INFO)
security_logger = logging.getLogger("security")

failed_attempts = {}
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 900


class UsersOpration:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, username: str, password: str, fullname: str, phone: str, email: str, address: str) -> User:
        user = User(username=username, password=password, fullname=fullname, phone=phone, email=email, address=address)
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
        await self.get_by_username(username)
        query = sa.delete(User).where(User.username == username)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def login(self, username: str, password: str) -> JWTResponsePayload:
        current_time = datetime.now()
        client_ip = "unknown"

        dangerous_patterns = ["'", "\"", ";", "--", "/*", "*/", "xp_", "union select", "drop table", "insert into",
                              "update set", "delete from"]
        if any(pattern in username.lower().replace(" ", "") for pattern in dangerous_patterns):
            security_logger.warning(f"SQL_INJECTION_BLOCKED - username: {username}")
            raise exceptions.UsernameOrPasswordIncorrect
        if any(pattern in password.lower().replace(" ", "") for pattern in dangerous_patterns):
            security_logger.warning(f"SQL_INJECTION_BLOCKED - password: {password}")
            raise exceptions.UsernameOrPasswordIncorrect

        if username in failed_attempts:
            last_attempt_time, attempts = failed_attempts[username]
            if attempts >= MAX_ATTEMPTS:
                time_elapsed = (current_time - last_attempt_time).total_seconds()
                if time_elapsed < LOCKOUT_TIME:
                    remaining_time = LOCKOUT_TIME - time_elapsed
                    security_logger.warning(
                        f"BRUTE_FORCE_BLOCKED - Account temporarily locked "
                        f"- username: {username} "
                        f"- attempts: {attempts} "
                        f"- time_remaining: {int(remaining_time)}s"
                    )
                    raise exceptions.UsernameOrPasswordIncorrect

        login_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        query = sa.select(User).where(User.username == username)
        async with self.db_session as session:
            user = await session.scalar(query)
            if user is None:
                if username in failed_attempts:
                    last_time, attempts = failed_attempts[username]
                    failed_attempts[username] = (current_time, attempts + 1)
                else:
                    failed_attempts[username] = (current_time, 1)

                security_logger.warning(
                    f"SECURITY_ALERT - Failed login: User not found "
                    f"- username: {username} "
                    f"- time: {login_time} "
                    f"- ip: {client_ip}"
                )
                raise exceptions.UsernameOrPasswordIncorrect

        if not password_manager.verify(password, user.password):
            if username in failed_attempts:
                last_time, attempts = failed_attempts[username]
                failed_attempts[username] = (current_time, attempts + 1)
            else:
                failed_attempts[username] = (current_time, 1)

            security_logger.warning(
                f"SECURITY_ALERT - Failed login: Invalid password "
                f"- username: {username} "
                f"- time: {login_time} "
                f"- ip: {client_ip}"
            )
            raise exceptions.UsernameOrPasswordIncorrect

        if username in failed_attempts:
            del failed_attempts[username]

        security_logger.info(
            f"SUCCESS - User login "
            f"- username: {username} "
            f"- time: {login_time} "
            f"- ip: {client_ip}"
        )
        return JWTHandler.generate(username)
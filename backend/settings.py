import os
from passlib.context import CryptContext

password_manager = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY: str = "MySuperSecureKey_For_Hackathon_2024@ََASA!"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
ALGORITHM: str = "HS512"
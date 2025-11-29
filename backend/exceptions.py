from fastapi.exceptions import HTTPException
from starlette import status
import logging

security_logger = logging.getLogger("security")

class UserNotFound(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "User not found!"
        security_logger.warning("SECURITY - UserNotFound exception raised")

class UserAlreadyExist(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "User already exist!"
        security_logger.warning("SECURITY - UserAlreadyExist exception raised")

class UsernameOrPasswordIncorrect(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Username or password incorrect!"
        security_logger.warning("SECURITY - UsernameOrPasswordIncorrect exception raised")
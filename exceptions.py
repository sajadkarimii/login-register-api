from fastapi.exceptions import HTTPException
from starlette import status


class UserNotFound(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "User not found!"

class UserAlreadyExist(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "User already exist!"

class UsernameOrPasswordIncorrect(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Username or password incorrect ..."
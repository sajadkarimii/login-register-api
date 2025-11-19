from pydantic import BaseModel

class RegisterInput(BaseModel):
    username: str
    password: str
    fullname: str
    phone: str
    email: str
    address: str

class DeleteUserInput(BaseModel):
    username: str
    password: str
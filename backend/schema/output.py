from pydantic import BaseModel

class UserOutput(BaseModel):
    username: str
    fullname: str
    phone: str
    email: str | None
    address: str | None

    class Config:
        orm_mode = True

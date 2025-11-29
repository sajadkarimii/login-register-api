from pydantic import BaseModel, EmailStr, constr, validator
import re

PASSWORD_MIN = 8
PASSWORD_MAX = 72


class RegisterInput(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=PASSWORD_MIN, max_length=PASSWORD_MAX)
    fullname: constr(min_length=3, max_length=100)
    phone: constr(min_length=10, max_length=15)
    email: EmailStr
    address: constr(min_length=1, max_length=200)

    class Config:
        extra = "forbid"

    @validator('password')
    def password_strength(cls, v):
        weak_passwords = [
            '12345678', 'password', '123456789', '1234567890',
            'qwerty', 'abc123', 'password1', '12345', '1234',
            '111111', '000000', 'admin', 'letmein'
        ]

        if v.lower() in weak_passwords:
            raise ValueError('Password is too common and weak. Choose a stronger password.')

        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter (A-Z)')

        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter (a-z)')

        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit (0-9)')

        return v

    @validator('phone')
    def phone_validator(cls, v):
        if not re.match(r'^\+?[\d]+$', v):
            raise ValueError('Phone number must contain only numbers, + or 0')
        return v

class LoginInput(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=PASSWORD_MIN, max_length=PASSWORD_MAX)

    class Config:
        extra = "forbid"
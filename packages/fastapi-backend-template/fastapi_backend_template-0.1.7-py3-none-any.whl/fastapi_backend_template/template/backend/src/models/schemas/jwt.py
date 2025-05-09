import datetime

from pydantic import BaseModel, EmailStr


class JWToken(BaseModel):
    exp: datetime.datetime
    sub: str


class JWTAccount(BaseModel):
    username: str
    email: EmailStr

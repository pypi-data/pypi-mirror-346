import datetime

from pydantic import EmailStr

from src.models.schemas.base import BaseSchemaModel


class AccountInCreate(BaseSchemaModel):
    username: str
    email: EmailStr
    password: str


class AccountInUpdate(BaseSchemaModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class AccountInLogin(BaseSchemaModel):
    username: str
    email: EmailStr
    password: str


class AccountWithToken(BaseSchemaModel):
    token: str
    username: str
    email: EmailStr
    is_verified: bool
    is_active: bool
    is_logged_in: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime | None = None


class AccountInResponse(BaseSchemaModel):
    id: int
    authorized_account: AccountWithToken

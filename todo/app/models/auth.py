from sqlmodel import SQLModel
from pydantic import SecretStr


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class ChangePassword(SQLModel):
    new_password: SecretStr

from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr, SecretStr
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.todo import Todo


class BaseUser(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str


class User(BaseUser, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    todos: list["Todo"] = Relationship(back_populates="user")


class CreateUser(BaseUser):
    password: SecretStr
    email: EmailStr


class CreatedUser(BaseUser):
    id: int
    created_at: datetime
    updated_at: datetime


class CurrentUser(CreatedUser):
    pass


class UpdateUser(SQLModel):
    name: str


class UpdatedUser(CreatedUser):
    pass

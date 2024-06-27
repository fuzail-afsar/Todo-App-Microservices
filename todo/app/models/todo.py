from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.user import User


class BaseTodo(SQLModel):
    content: str = Field(index=True)


class Todo(BaseTodo, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="todos")


class CreateTodo(SQLModel):
    content: str


class UpdateTodo(CreateTodo):
    pass

from app.api.deps import Pagination, VerifyToken
from fastapi import APIRouter, status, HTTPException

from app.core.db import DB
from app.models.todo import CreateTodo, UpdateTodo, Todo
from app.crud import todo as todoCrud

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(user: VerifyToken, todo: CreateTodo, db: DB) -> Todo:
    todo_created = todoCrud.create(user.id, todo, db)

    if not todo_created:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid request data",
        )

    return todo_created


@router.get("/")
def get_todos(user: VerifyToken, db: DB, pagination: Pagination) -> list[Todo]:
    return todoCrud.fetch_user_todos(user.id, db, **pagination)


@router.get("/{id}")
def get_todo(user: VerifyToken, id: int, db: DB) -> Todo:
    todo = todoCrud.fetch_user_todo(user.id, id, db)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return todo


@router.patch("/{id}")
def update_todo(user: VerifyToken, id: str, update_todo: UpdateTodo, db: DB) -> Todo:
    todo = todoCrud.update_by_id(user.id, id, update_todo, db)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return todo


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: VerifyToken, id: str, db: DB):
    isDeleted = todoCrud.delete_by_id(user.id, id, db)

    if not isDeleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_todos(user: VerifyToken, db: DB):
    isDeleted = todoCrud.delete_all(user.id, db)

    if not isDeleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todos not found"
        )

    return

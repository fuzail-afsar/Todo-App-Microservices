from sqlmodel import select, delete

from app.core.db import DB
from app.models.todo import CreateTodo, Todo, UpdateTodo


def create(user_id: int, todo: CreateTodo, db: DB) -> Todo:
    try:
        todo_created: Todo = Todo.model_validate(todo, update={"user_id": user_id})

        db.add(todo_created)
        db.commit()
        db.refresh(todo_created)

        return todo_created
    except Exception as e:
        print("Exception:", e)
        return None


def fetch_user_todos(user_id: int, db: DB, offset: int = 0, limit: int = 100):
    try:
        todos: list[Todo] = db.exec(
            select(Todo).where(Todo.user_id == user_id).offset(offset).limit(limit)
        ).all()

        return todos
    except Exception as e:
        print("Exception:", e)
        return None


def fetch_user_todo(user_id: int, id: int, db: DB):
    try:
        todo: Todo = db.exec(
            select(Todo).where(Todo.user_id == user_id and Todo.id == id)
        ).one()

        return todo
    except Exception as e:
        print("Exception:", e)
        return None


def update_by_id(user_id: int, id: int, data: UpdateTodo, db: DB):
    try:
        todo = fetch_user_todo(user_id, id, db)

        if not todo:
            return None

        updated_data = data.model_dump(exclude_unset=True)
        todo.sqlmodel_update(updated_data)

        db.add(todo)
        db.commit()
        db.refresh(todo)

        return todo
    except Exception as e:
        print("Exception:", e)
        return None


def delete_by_id(user_id: int, id: int, db: DB):
    try:
        db.exec(delete(Todo).where(Todo.user_id == user_id and Todo.id == id))
        db.commit()

        return True
    except Exception as e:
        print("Exception:", e)
        return None


def delete_all(user_id: int, db: DB):
    try:
        db.exec(delete(Todo).where(Todo.user_id == user_id))
        db.commit()

        return True
    except Exception as e:
        print("Exception:", e)
        return None

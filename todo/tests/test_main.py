from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session


from app.main import app
from app.core.config import settings
from app.core.db import init_db, get_session

connection_string = str(settings.TEST_DATABASE_URL)

engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

init_db(engine)


def get_session_override():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = get_session_override
client = TestClient(app=app)


def test_create_todo():
    todo_content = "test create todo"

    response = client.post("/api/todos/", json={"content": todo_content})
    data = response.json()

    assert response.status_code == 200
    assert data["content"] == todo_content


def test_get_todos():
    response = client.get("/api/todos/")
    assert response.status_code == 200


def test_update_todo():
    todo_content = "update todo"

    response = client.post("/api/todos/", json={"content": todo_content})
    assert response.status_code == 200

    data = response.json()
    todoId = data["id"]
    updated_content = "updated todo"

    updated_response = client.patch(
        f"/api/todos/{todoId}", json={"content": updated_content}
    )
    updated_data = updated_response.json()

    assert updated_response.status_code == 200
    assert updated_data["id"] == todoId
    assert updated_data["content"] == updated_content


def test_delete_todo():
    todo_content = "test delete todo"

    response = client.post("/api/todos/", json={"content": todo_content})
    assert response.status_code == 200

    data = response.json()
    todo_id = data["id"]

    response = client.delete(f"/api/todos/{todo_id}")
    assert response.status_code == 200

    response = client.get("/api/todos")
    todos = response.json()

    assert all(todo["id"] != todo_id for todo in todos)


def test_delete_all_todos():
    todo_content = "test delete all todos"

    response = client.post("/api/todos/", json={"content": todo_content})
    assert response.status_code == 200

    response = client.delete("/api/todos/")
    assert response.status_code == 200

    response = client.get("/api/todos")
    todos = response.json()

    assert len(todos) == 0

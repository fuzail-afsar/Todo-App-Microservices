from fastapi import APIRouter

from app.api.routes import todos, users, auth

api_router = APIRouter()
api_router.include_router(todos.router, prefix="/todos", tags=["Todos"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])

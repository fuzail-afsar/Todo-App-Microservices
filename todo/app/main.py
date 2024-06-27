from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.db import init_db, DB
from app.api.main import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables...")
    init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    servers=[{"url": settings.url, "description": settings.DESCRIPTION}],
)

app.include_router(api_router, prefix=settings.PREFIX)

from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

from app.core.config import settings


connection_string = str(settings.DATABASE_URL)

engine = create_engine(connection_string, pool_recycle=300)


def init_db(engine=engine) -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        raise e


DB = Annotated[Session, Depends(get_session)]

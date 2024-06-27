from datetime import datetime
from pydantic import EmailStr, SecretStr
from sqlmodel import select

from app.core.db import DB
from app.models.user import CreateUser, User
from app.lib.passlib import get_password_hash, verify_password


def create(user: CreateUser, db: DB):
    try:
        user_created: User = User.model_validate(
            user,
            update={
                "hashed_password": get_password_hash(user.password.get_secret_value())
            },
        )

        db.add(user_created)
        db.commit()
        db.refresh(user_created)

        return user_created
    except Exception as e:
        print("Exception:", e)
        return None


def get_user_by_email(email: EmailStr, db: DB):
    try:
        statement = select(User).where(User.email == email)
        user: User = db.exec(statement).first()
        if user:
            return user
        return None
    except Exception as e:
        print("Exception:", e)
        return None


def authenticate(email: EmailStr, password: str | SecretStr, db: DB):
    try:
        pwd = (
            password.get_secret_value() if isinstance(password, SecretStr) else password
        )

        db_user = get_user_by_email(email, db)

        if not db_user:
            return None
        if not verify_password(pwd, db_user.hashed_password):
            return None
        return db_user
    except Exception as e:
        print("Exception:", e)
        return None


def change_password(user: User, new_password: str | SecretStr, db: DB):
    try:
        pwd = (
            new_password.get_secret_value()
            if isinstance(new_password, SecretStr)
            else new_password
        )

        user.hashed_password = get_password_hash(pwd)
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except Exception as e:
        print("Exception:", e)
        return None


def update(user: User, data, db: DB):
    try:
        updated_data = data.model_dump(exclude_unset=True)
        updated_data["updated_at"] = datetime.now()
        print("updated_data", updated_data)
        user.sqlmodel_update(updated_data)
        print("user", user)
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    except Exception as e:
        print("Exception:", e)
        return None

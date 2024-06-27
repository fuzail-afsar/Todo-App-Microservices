from typing import Annotated
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.lib import jose
from app.core.db import DB
from app.crud import user as userCrud
from app.models.auth import Token, ChangePassword
from app.models.response import Message
from app.api.deps import VerifyToken

router = APIRouter()


@router.post("/token", status_code=status.HTTP_201_CREATED)
def login_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
    db: DB,
) -> Token:
    user = userCrud.authenticate(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    elif not user.is_active:
        raise HTTPException(status=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return Token(
        access_token=jose.create_access_token(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "is_active": user.is_active,
            }
        )
    )


@router.post("/change-password")
def change_password(body: ChangePassword, user: VerifyToken, db: DB) -> Message:
    updated_user = userCrud.change_password(user, body.new_password, db)
    if not updated_user:
        raise HTTPException(
            status=status.HTTP_400_BAD_REQUEST, detail="Password update failed"
        )

    return Message(message="Password updated successfully")

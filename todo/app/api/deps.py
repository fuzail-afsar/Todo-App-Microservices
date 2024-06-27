from app.lib import jose
from fastapi import Query, Depends, status, HTTPException

from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from app.core.db import DB
from app.models.auth import Token
from app.core.config import settings
from app.crud import user as userCrud
from app.models.user import User


def pagination(offset: int = 0, limit: int = Query(default=100, le=100)):
    return {"offset": offset, "limit": limit}


Pagination = Annotated[dict, Depends(pagination)]


oauth2_token = OAuth2PasswordBearer(tokenUrl=f"{settings.PREFIX}/auth/token")
OAuth2Token = Annotated[Token, Depends(oauth2_token)]


def verify_token(token: OAuth2Token, db: DB):
    decoded_token = jose.decode_token(token)

    print("decoded_token", decoded_token)
    if not decoded_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = userCrud.get_user_by_email(decoded_token["data"]["email"], db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist.",
        )
    elif not user.is_active:
        raise HTTPException(status=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return user


VerifyToken = Annotated[User, Depends(verify_token)]

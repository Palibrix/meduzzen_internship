from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import WrongPasswordOrEmail
from app.db.database import get_session
from app.schemas.token_schema import Token
from app.services.authentication_service import AuthenticationService

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_session)
):
    service = AuthenticationService(db)
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise WrongPasswordOrEmail
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = service.create_access_token(
        data={"sub": user.user_email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_session
from app.schemas.token_schema import Token
from app.schemas import user_schema as schemas
from app.services.authentication_service import AuthenticationService
from app.services.user_service import UserService

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_session)
):
    service = AuthenticationService(db)
    access_token = await service.authenticate_user(form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.User)
async def read_users_me(
        token: str = Depends(settings.oauth2_scheme),
        db: AsyncSession = Depends(get_session)
):
    service = UserService(db)
    return await service.get_current_user(token)

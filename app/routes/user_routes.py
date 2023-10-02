from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.schemas import user_schema as schemas
from app.services.user_service import UserService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/users/", response_model=schemas.UsersListResponse)
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    service = UserService(db)
    return {"users": await service.get_all_users(skip=skip, limit=limit)}


@router.get("/users/{user_id}", response_model=schemas.UserDetailResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    service = UserService(db)
    return await service.get_one_user(user_id=user_id)


@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    ...


@router.post("/sign-up/", response_model=schemas.SignUpRequest)
async def create_user(user: schemas.SignUpRequest, db: AsyncSession = Depends(get_session)):
    service = UserService(db)
    return await service.create_user(user=user)


@router.put("/users/{user_id}", response_model=schemas.UserUpdateRequest)
async def update_user(user_id: int, user: schemas.UserUpdateRequest, db: AsyncSession = Depends(get_session)):
    service = UserService(db)
    return await service.update_user(user_id=user_id, user=user)


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    service = UserService(db)
    return await service.delete_user(user_id=user_id)

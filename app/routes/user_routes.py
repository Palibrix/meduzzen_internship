from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import user_schema as schemas
from app.models import user_model as model

from app.db.database import get_session
from app.services import user_service

router = APIRouter()


@router.get("/users/", response_model=schemas.UsersListResponse)
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(model.User).offset(skip).limit(limit))
    users = result.scalars().all()
    return {"users": users}


@router.get("/users/{user_id}", response_model=schemas.UserDetailResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    # noinspection PyTypeChecker
    user = await user_service.get_one_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                            )
    return user


@router.post("/sign-up/", response_model=schemas.SignUpRequest)
async def create_user(user: schemas.SignUpRequest, db: AsyncSession = Depends(get_session)):
    db_user = await user_service.get_one_user(db=db, email=user.user_email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="User with this email already exist"
                            )
    new_user = await user_service.create_user(db, user)
    return new_user


@router.put("/users/{user_id}", response_model=schemas.UserUpdateRequest)
async def update_user(user_id: int, user: schemas.UserUpdateRequest, db: AsyncSession = Depends(get_session)):
    db_user = await user_service.get_one_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                            )
    db_user = await user_service.update_user(db=db, db_user=db_user, user=user)
    return db_user


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    db_user = await user_service.get_one_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                            )
    await db.delete(db_user)
    await db.commit()
    return {"detail": "User deleted"}

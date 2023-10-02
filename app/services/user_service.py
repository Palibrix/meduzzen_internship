from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from app.models import user_model as model
from app.schemas import user_schema as schemas


class UserService:

	def __init__(self, db: AsyncSession):
		self.db = db

	async def get_all_users(self, skip: int, limit: int):
		result = await self.db.execute(select(model.User).offset(skip).limit(limit))
		return result.scalars().all()

	async def get_one_user(self, user_id: int = None, email: str = None):
		if not user_id and not email:
			raise ValueError("Either 'id' or 'email' must be provided")
		email = email.lower() if email else None
		stmt = select(model.User).where(or_(model.User.user_id == user_id, model.User.user_email == email))
		result = await self.db.execute(stmt)
		user = result.scalars().first()

		if user is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
								detail="User not found"
								)

		return user

	async def create_user(self, user: schemas.SignUpRequest):
		pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

		try:
			await self.get_one_user(email=user.user_email)
		except HTTPException as e:
			if e.status_code == status.HTTP_404_NOT_FOUND:
				...
		else:
			raise HTTPException(status_code=status.HTTP_409_CONFLICT,
								detail="User with this email already exist"
								)

		normalized_email = user.user_email.lower()
		hashed_password = pwd_context.hash(user.hashed_password)

		user_dict = user.model_dump()

		user_dict["user_email"] = normalized_email
		user_dict["hashed_password"] = hashed_password

		new_user = model.User(**user_dict)
		self.db.add(new_user)
		await self.db.commit()
		await self.db.refresh(new_user)
		return new_user

	async def update_user(self, user_id: int, user: schemas.UserUpdateRequest):
		db_user = await self.get_one_user(user_id=user_id)
		for key, value in user.model_dump().items():
			if value is not None:
				setattr(db_user, key, value)
		await self.db.commit()
		return db_user

	async def delete_user(self, user_id: int):
		db_user = await self.get_one_user(user_id=user_id)
		await self.db.delete(db_user)
		await self.db.commit()
		return {"detail": "User deleted"}


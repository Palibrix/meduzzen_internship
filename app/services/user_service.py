import secrets
import string
from typing import Annotated

from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import UserNotFound, UserExist, CredentialsException, InactiveUser
from app.models import user_model as model
from app.schemas import user_schema as schemas
from app.schemas import token_schema


class UserService:

	def __init__(self, db: AsyncSession):
		self.db = db

	async def get_one_user_result(self, user_id: int = None, email: str = None):
		if not user_id and not email:
			raise ValueError("Either 'id' or 'email' must be provided")
		email = email.lower() if email else None
		stmt = select(model.User).where(or_(model.User.user_id == user_id, model.User.user_email == email))
		result = await self.db.execute(stmt)
		return result.scalars().first()

	async def get_all_users(self, skip: int, limit: int):
		result = await self.db.execute(select(model.User).offset(skip).limit(limit))
		return result.scalars().all()

	async def get_one_user(self, user_id: int = None, email: str = None):

		user = await self.get_one_user_result(user_id=user_id, email=email)

		if user is None:
			raise UserNotFound

		return user

	async def create_user(self, user: schemas.SignUpRequest):

		db_user = await self.get_one_user_result(email=user.user_email)
		if db_user:
			raise UserExist

		normalized_email = self.normalize_email(user.user_email)
		hashed_password = self.get_password_hash(user.hashed_password)

		user_dict = user.model_dump()

		user_dict["user_email"] = normalized_email
		user_dict["hashed_password"] = hashed_password

		new_user = model.User(**user_dict)
		self.db.add(new_user)
		await self.db.commit()
		await self.db.refresh(new_user)
		return new_user

	async def create_user_by_email(self, email, firstname, lastname):
		password = ""
		for _ in range(9):
			password += secrets.choice(string.ascii_lowercase)
		new_user = model.User(user_email=email, user_firstname=firstname, user_lastname=lastname,
							hashed_password=password)

		normalized_email = self.normalize_email(new_user.user_email)
		hashed_password = self.get_password_hash(new_user.hashed_password)

		new_user.user_email = normalized_email
		new_user.hashed_password = hashed_password

		self.db.add(new_user)
		await self.db.commit()
		await self.db.refresh(new_user)
		return new_user

	async def update_user(self, user_id: int, user: schemas.UserUpdateRequest):
		db_user = await self.get_one_user(user_id=user_id)
		for key, value in user.model_dump().items():
			if value is not None:
				if key == "hashed_password":
					value = self.get_password_hash(value)
				setattr(db_user, key, value)
		await self.db.commit()
		return db_user

	async def delete_user(self, user_id: int):
		db_user = await self.get_one_user(user_id=user_id)
		await self.db.delete(db_user)
		await self.db.commit()
		return {"detail": "User deleted"}

	async def get_current_user(self, token: str):
		try:

			payload = jwt.decode(token=token, key=settings.secret_key,
								audience=settings.audience, algorithms=[settings.algorithm])
			email: str = payload.get("email") or payload.get("sub")

			if email is None or "@" not in email:
				raise CredentialsException
			token_data = token_schema.TokenData(email=email)
		except JWTError:
			raise CredentialsException
		user = await self.get_one_user_result(email=token_data.email)
		if not user:
			firstname = payload.get("firstname")
			lastname = payload.get("lastname")
			if not firstname and not lastname:
				raise CredentialsException
			user = await self.create_user_by_email(email=email, firstname=firstname, lastname=lastname)
		if not user.is_active:
			raise InactiveUser
		return user

	@staticmethod
	def verify_password(plain_password, hashed_password):
		return settings.pwd_context.verify(plain_password, hashed_password)

	@staticmethod
	def get_password_hash(password):
		return settings.pwd_context.hash(password)

	@staticmethod
	def normalize_email(email):
		return email.lower()

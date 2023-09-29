from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from app.models import user_model as model
from app.schemas import user_schema as schemas


async def get_one_user(db: AsyncSession, user_id: int = None, email: str = None):
	if user_id is None and email is None:
		raise ValueError("Either 'id' or 'email' must be provided")
	email = email.lower() if email else None
	stmt = select(model.User).where(or_(model.User.user_id == user_id, model.User.user_email == email))
	result = await db.execute(stmt)
	user = result.scalars().first()

	return user


async def create_user(db: AsyncSession, user: schemas.SignUpRequest):
	pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

	normalized_email = user.user_email.lower()
	hashed_password = pwd_context.hash(user.hashed_password)

	user_dict = user.model_dump()

	user_dict["user_email"] = normalized_email
	user_dict["hashed_password"] = hashed_password

	new_user = model.User(**user_dict)
	db.add(new_user)
	await db.commit()
	await db.refresh(new_user)
	return new_user


async def update_user(db: AsyncSession, db_user, user: schemas.UserUpdateRequest):
	for key, value in user.model_dump().items():
		if value is not None:
			setattr(db_user, key, value)
	await db.commit()
	return db_user

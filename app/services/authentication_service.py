from datetime import timedelta, datetime

from jose import jwt

from app.core.config import settings
from app.core.exceptions import WrongPasswordOrEmail
from app.services.user_service import UserService


class AuthenticationService:
	def __init__(self, db):
		self.db = db

	async def authenticate_user(self, email: str, password: str):
		user_service = UserService(self.db)
		user = await user_service.get_one_user(email=email)
		if not user_service.verify_password(password, user.hashed_password):
			raise WrongPasswordOrEmail
		if not user:
			raise WrongPasswordOrEmail
		access_token = self.create_access_token(
			data={"sub": user.user_email}, expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
		)
		return access_token

	@staticmethod
	def create_access_token(data: dict, expires_delta: timedelta | None = None):
		to_encode = data.copy()
		if expires_delta:
			expire = datetime.utcnow() + expires_delta
		else:
			expire = datetime.utcnow() + timedelta(minutes=15)
		to_encode.update({"exp": expire})
		encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
		return encoded_jwt

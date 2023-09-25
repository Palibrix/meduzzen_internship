from sqlalchemy import Boolean, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
	__tablename__ = "users"

	user_id = Column(Integer, primary_key=True, index=True, nullable=False)
	user_email = Column(String, unique=True, index=True, nullable=False)
	user_firstname = Column(String, nullable=False)
	user_lastname = Column(String, nullable=False)
	user_city = Column(String)
	user_phone = Column(String)
	user_avatar = Column(String)

	hashed_password = Column(String)

	is_active = Column(Boolean(), default=True)
	is_superuser = Column(Boolean(), default=False)

	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())

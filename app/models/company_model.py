from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey

from app.db.database import Base


class Company(Base):
	__tablename__ = "companies"

	company_id = Column(Integer, primary_key=True, index=True, nullable=False)
	company_owner_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
	company_name = Column(String(30), unique=True, nullable=False)
	company_title = Column(String(70), nullable=False)
	company_description = Column(String, nullable=False)
	company_city = Column(String)
	company_phone = Column(String)
	company_links = Column(String)
	company_avatar = Column(String)

	is_visible = Column(Boolean(), nullable=False, default=True)

	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())

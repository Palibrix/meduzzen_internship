from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class CompanyMembers(Base):
	__tablename__ = 'company_members'

	user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
	company_id = Column(Integer, ForeignKey('companies.company_id'), primary_key=True)

	is_admin = Column(Boolean(), default=False)


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

	company_members = relationship("User", secondary=CompanyMembers.__table__, backref="companies", lazy='joined')

	is_visible = Column(Boolean(), nullable=False, default=True)

	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())

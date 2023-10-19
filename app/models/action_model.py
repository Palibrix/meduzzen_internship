from sqlalchemy import Column, Integer, ForeignKey, func, DateTime, Enum

from app.db.database import Base


class Action(Base):
	__tablename__ = 'actions'

	action_id = Column(Integer, primary_key=True, index=True, nullable=False)
	user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
	company_id = Column(Integer, ForeignKey('companies.company_id', ondelete='CASCADE'), nullable=False)
	action = Column(Enum('request', 'invite', name='action_type'), nullable=False)

	created_at = Column(DateTime(timezone=True), server_default=func.now())

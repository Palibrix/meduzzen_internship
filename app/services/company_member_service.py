from sqlalchemy import select, and_

from app.core.exceptions import ObjectNotFound
from app.models.company_model import CompanyMembers


class CompanyMemberService:

	def __init__(self, db):
		self.db = db

	async def get_one_member_result(self, company_id, user_id):
		stmt = select(CompanyMembers).where(
			and_(
				CompanyMembers.company_id == company_id,
				CompanyMembers.user_id == user_id
			)
		)
		result = await self.db.execute(stmt)
		return result.scalars().first()

	async def get_one_member(self, company_id, user_id):
		member = await self.get_one_member_result(company_id=company_id, user_id=user_id)

		if member is None:
			raise ObjectNotFound

		return member

	async def get_all_members(self, company_id):
		stmt = select(CompanyMembers).where(
			CompanyMembers.company_id == company_id  # type: ignore
		)
		result = await self.db.execute(stmt)

		return result.scalars().all()

	async def get_all_admins(self, company_id):
		stmt = select(CompanyMembers).where(
			and_(
				CompanyMembers.company_id == company_id,
				CompanyMembers.is_admin == True
			)
		)
		result = await self.db.execute(stmt)

		return result.scalars().all()

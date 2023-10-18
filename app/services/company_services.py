from sqlalchemy import select, or_, and_

from app.core.exceptions import ObjectNotFound, CompanyExist
from app.models.company_model import Company
from app.services.user_service import UserService
from app.schemas import company_schema as schemas


class CompanyService:

	def __init__(self, db):
		self.db = db

	async def get_all_companies(self, skip: int, limit: int, token):
		user_service = UserService(self.db)
		active_user = await user_service.get_current_user(token=token)

		stmt = select(Company).where(or_(Company.is_visible, Company.company_owner_id == active_user.user_id)).offset(skip).limit(limit)
		result = await self.db.execute(stmt)
		return result.scalars().all()

	async def get_one_company_result(self, token, company_id: int = None, company_name: str = None):
		user_service = UserService(self.db)
		active_user = await user_service.get_current_user(token=token)

		if not company_name and not company_id:
			raise ValueError("Either 'id' or 'name' must be provided")
		stmt = select(Company).where(
			and_(
				or_(
					Company.is_visible,
					Company.company_owner_id == active_user.user_id,
				),
				or_(
					Company.company_id == company_id,
					Company.company_name == company_name,
				)
			)
		)
		result = await self.db.execute(stmt)
		return result.scalars().first()

	async def get_one_company(self, company_id, token):
		company = await self.get_one_company_result(company_id=company_id, token=token)

		if company is None:
			raise ObjectNotFound

		return company

	async def create_company(self, company, token):
		db_company = await self.get_one_company_result(company_name=company.company_name, token=token)
		if db_company:
			raise CompanyExist

		user_service = UserService(self.db)
		active_user = await user_service.get_current_user(token=token)

		company_dict = company.model_dump()
		company_dict['company_owner_id'] = active_user.user_id

		new_company = Company(**company_dict)
		self.db.add(new_company)
		await self.db.commit()
		await self.db.refresh(new_company)

		return company

	async def update_company(self, company_id: int, company: schemas.CompanyUpdateRequest, token):
		db_company = await self.get_one_company(company_id=company_id, token=token)
		for key, value in company.model_dump(exclude_none=True).items():
			setattr(db_company, key, value)
		await self.db.commit()
		return db_company

	async def delete_company(self, company_id: int, token):
		db_company = await self.get_one_company(company_id=company_id, token=token)
		await self.db.delete(db_company)
		await self.db.commit()
		return {"detail": "Company deleted"}

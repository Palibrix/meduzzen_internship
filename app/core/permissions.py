from app.core.exceptions import WrongUser
from app.schemas.user_schema import User
from app.services.company_services import CompanyService
from app.services.user_service import UserService


class IsCurrentUser:

	def __init__(self, db, user_id, token):
		self.db = db
		self.user_id = user_id
		self.token = token
		self.service = UserService(db)

	async def __call__(self):
		current_user: User = await self.service.get_current_user(token=self.token)
		if self.user_id != current_user.user_id:
			raise WrongUser


class IsCompanyOwner:

	def __init__(self, db, company_id, token):
		self.db = db
		self.company_id = company_id
		self.token = token
		self.company_service = CompanyService(db)
		self.user_service = UserService(db)

	async def __call__(self):
		company = await self.company_service.get_one_company(company_id=self.company_id, token=self.token)
		current_user: User = await self.user_service.get_current_user(token=self.token)
		if company.company_owner_id != current_user.user_id:
			raise WrongUser

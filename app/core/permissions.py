from app.core.exceptions import WrongUser
from app.models.company_model import Company, CompanyMembers
from app.schemas.user_schema import User
from app.services.action_service import ActionService
from app.services.company_member_service import CompanyMemberService
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


class IsCompanyOwnerOrAdmin:

	def __init__(self, db, company_id, token):
		self.db = db
		self.company_id = company_id
		self.token = token
		self.company_service = CompanyService(db)
		self.user_service = UserService(db)
		self.member_service = CompanyMemberService(db)

	async def __call__(self):
		company: Company = await self.company_service.get_one_company(company_id=self.company_id, token=self.token)
		current_user: User = await self.user_service.get_current_user(token=self.token)
		company_member: CompanyMembers = await self.member_service.get_one_member_result(company_id=company.company_id,
																				user_id=current_user.user_id)
		if company.company_owner_id == current_user.user_id or (company_member and company_member.is_admin):
			return True
		else:
			raise WrongUser


class IsInvited:

	def __init__(self, db, invitation_id, token):
		self.db = db
		self.invitation_id = invitation_id
		self.token = token
		self.action_service = ActionService(db)
		self.user_service = UserService(db)

	async def __call__(self):
		action = await self.action_service.get_one_action(action_id=self.invitation_id)
		current_user: User = await self.user_service.get_current_user(token=self.token)
		if action.user_id != current_user.user_id:
			raise WrongUser

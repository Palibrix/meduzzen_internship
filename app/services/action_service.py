from sqlalchemy import select, and_, or_

from app.core.exceptions import ActionExist, ObjectNotFound, MemberExist
from app.models.action_model import Action
from app.models.company_model import CompanyMembers
from app.schemas import action_schema as schemas
from app.services.company_member_service import CompanyMemberService
from app.services.company_services import CompanyService
from app.services.user_service import UserService


class ActionService:

	def __init__(self, db):
		self.db = db

	async def get_one_action_result(self, company_id: int, user_id: int, action: str, action_id: int = 0):

		if action not in (schemas.ActionType.request, schemas.ActionType.invite, None):
			raise ValueError('Wrong action')

		stmt = select(Action).where(
			or_(
				Action.action_id == action_id,
				and_(
					Action.company_id == company_id,
					Action.user_id == user_id,
					Action.action == action
				)
			)
		)
		result = await self.db.execute(stmt)
		return result.scalars().first()

	async def get_one_action(self, company_id: int = None, user_id: int = None,
							action: str = None, action_id: int = 0):

		action = await self.get_one_action_result(company_id=company_id, user_id=user_id,
												action=action, action_id=action_id)

		if action is None:
			raise ObjectNotFound

		return action

	async def get_actions(self):
		stmt = select(Action)
		result = await self.db.execute(stmt)
		return result.scalars().all()

	async def create_action(self, company_id, action, user_id=None, token=None):

		if action == schemas.ActionType.request:
			user_service = UserService(self.db)
			active_user = await user_service.get_current_user(token=token)
			user_id = active_user.user_id

		db_action = await self.get_one_action_result(company_id=company_id, user_id=user_id, action=action)
		if db_action:
			raise ActionExist

		member_service = CompanyMemberService(self.db)
		db_company_member = await member_service.get_one_member(company_id=company_id, user_id=user_id)

		if db_company_member:
			raise MemberExist

		new_action = Action(company_id=company_id, user_id=user_id, action=action)
		self.db.add(new_action)
		await self.db.commit()
		await self.db.refresh(new_action)

		return new_action

	async def delete_action(self, action_id):
		db_company = await self.get_one_action(action_id=action_id)
		await self.db.delete(db_company)
		await self.db.commit()
		return {"detail": "Action deleted"}

	async def accept_action(self, invitation_id):
		invitation = await self.get_one_action(action_id=invitation_id)

		company_member = CompanyMembers(user_id=invitation.user_id, company_id=invitation.company_id)

		self.db.add(company_member)
		await self.db.commit()
		await self.db.refresh(company_member)
		await self.delete_action(action_id=invitation_id)
		return {"detail": "Action accepted"}

	async def exclude_user(self, company_id: int, user_id: int):
		member_service = CompanyMemberService(self.db)
		member = await member_service.get_one_member(company_id=company_id, user_id=user_id)

		await self.db.delete(member)
		await self.db.commit()

		return {"detail": "User excluded from company"}

	async def leave_company(self, company_id: int, token: str):
		user_service = UserService(self.db)
		active_user = await user_service.get_current_user(token=token)

		return await self.exclude_user(company_id=company_id, user_id=active_user.user_id)

	async def view_requests(self, token: str):
		user_service = UserService(self.db)
		active_user = await user_service.get_current_user(token=token)

		stmt = select(Action).where(
			and_(
				Action.user_id == active_user.user_id,
				Action.action == schemas.ActionType.request
			)
		)
		result = await self.db.execute(stmt)

		return result.scalars().all()

	async def view_invitations(self, token: str):
		user_service = UserService(self.db)
		active_user = await user_service.get_current_user(token=token)

		stmt = select(Action).where(
			and_(
				Action.user_id == active_user.user_id,
				Action.action == schemas.ActionType.invite
			)
		)
		result = await self.db.execute(stmt)

		return result.scalars().all()

	async def view_invited_users(self, company_id: int):
		stmt = select(Action).where(
			and_(
				Action.company_id == company_id,
				Action.action == schemas.ActionType.invite
			)
		)
		result = await self.db.execute(stmt)

		return result.scalars().all()

	async def view_join_requests(self, company_id: int):
		stmt = select(Action).where(
			and_(
				Action.company_id == company_id,
				Action.action == schemas.ActionType.request
			)
		)
		result = await self.db.execute(stmt)

		return result.scalars().all()

	async def view_company_users(self, company_id: int):
		member_service = CompanyMemberService(self.db)
		return await member_service.get_all_members(company_id=company_id)

	async def change_admin(self, company_id, user_id):
		member_service = CompanyMemberService(self.db)
		member = await member_service.get_one_member(company_id=company_id, user_id=user_id)

		member.is_admin = not member.is_admin

		await self.db.commit()
		return member

	async def view_company_admins(self, company_id):
		member_service = CompanyMemberService(self.db)
		return await member_service.get_all_admins(company_id=company_id)

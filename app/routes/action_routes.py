from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.permissions import IsCompanyOwner, IsInvited
from app.db.database import get_session
from app.schemas import action_schema as schemas
from app.services.action_service import ActionService

router = APIRouter()


@router.post("/companies/{company_id}/invitations", response_model=schemas.Action)
async def send_invitation(
		company_id: int,
		user_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.create_action(company_id=company_id, user_id=user_id, action='invite')


@router.post("/companies/{company_id}/requests", response_model=schemas.Action)
async def send_request(
		company_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	return await service.create_action(company_id=company_id, action='request', token=token)


@router.delete("/companies/{company_id}/invitations/{action_id}")
async def cancel_invitation(
		company_id: int,
		action_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.delete_action(action_id=action_id)


@router.post('/invitations/{action_id}/reject')
async def reject_invitation(
		action_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsInvited(db=db, token=token, invitation_id=action_id).__call__()
	return await service.delete_action(action_id=action_id)


@router.post('/invitations/{action_id}/accept')
async def accept_invitation(
		action_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsInvited(db=db, token=token, invitation_id=action_id).__call__()
	return await service.accept_action(invitation_id=action_id)


@router.post('/companies/{company_id}/requests/{action_id}/reject')
async def reject_request(
		action_id: int,
		company_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.delete_action(action_id=action_id)


@router.post('/companies/{company_id}/requests/{action_id}/accept')
async def accept_request(
		action_id: int,
		company_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.accept_action(invitation_id=action_id)


@router.delete("/request/{action_id}")
async def cancel_request(
		action_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsInvited(db=db, token=token, invitation_id=action_id).__call__()
	return await service.delete_action(action_id=action_id)


@router.delete("/companies/{company_id}/users/{user_id}")
async def exclude_user(
		company_id: int,
		user_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.exclude_user(company_id=company_id, user_id=user_id)


@router.put("/companies/{company_id}/users/{user_id}")
async def change_admin(
		company_id: int,
		user_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.change_admin(company_id=company_id, user_id=user_id)


@router.delete("/companies/{company_id}/leave")
async def leave_company(
		company_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	return await service.leave_company(company_id=company_id, token=token)


@router.get("/user/requests", response_model=schemas.ActionListResponse)
async def view_requests(
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	return await service.view_requests(token=token)


@router.get("/user/invitations", response_model=schemas.ActionListResponse)
async def view_invitations(
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	return await service.view_invitations(token=token)


@router.get("/companies/{company_id}/invitations", response_model=schemas.ActionListResponse)
async def view_invited_users(
		company_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.view_invited_users(company_id=company_id)


@router.get("/companies/{company_id}/requests", response_model=schemas.ActionListResponse)
async def view_join_requests(
		company_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.view_join_requests(company_id=company_id)


@router.get("/companies/{company_id}/users")
async def view_company_users(
		company_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.view_company_users(company_id=company_id)


@router.get("/companies/{company_id}/admins")
async def view_company_admins(
		company_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = ActionService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.view_company_admins(company_id=company_id)

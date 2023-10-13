from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.permissions import IsCurrentUser, IsCompanyOwner
from app.db.database import get_session
from app.schemas import company_schema as schemas
from app.services.company_services import CompanyService

router = APIRouter()


@router.get('/companies/', response_model=schemas.CompaniesListResponse)
async def get_companies(
		skip: int = 0, limit: int = 10,
		token: str = Depends(settings.oauth2_scheme),
		db: AsyncSession = Depends(get_session)
):
	service = CompanyService(db)
	return {"companies": await service.get_all_companies(skip=skip, limit=limit, token=token)}


@router.get('/companies/{company_id}', response_model=schemas.CompanyDetailResponse)
async def get_company(
		company_id: int,
		token: str = Depends(settings.oauth2_scheme),
		db: AsyncSession = Depends(get_session)
):
	service = CompanyService(db)
	return await service.get_one_company(company_id=company_id, token=token)


@router.post("/companies/create", response_model=schemas.CompanyCreateRequest)
async def create_company(
		company: schemas.CompanyCreateRequest,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = CompanyService(db)
	return await service.create_company(company=company, token=token)


@router.put("/companies/{company_id}", response_model=schemas.CompanyUpdateRequest)
async def update_company(
		company_id: int,
		company: schemas.CompanyUpdateRequest,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = CompanyService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.update_company(company_id=company_id, company=company, token=token)


@router.delete("/companies/{company_id}")
async def delete_company(
		company_id: int,
		db: AsyncSession = Depends(get_session),
		token: str = Depends(settings.oauth2_scheme)
):
	service = CompanyService(db)
	await IsCompanyOwner(db=db, token=token, company_id=company_id).__call__()
	return await service.delete_company(company_id=company_id, token=token)

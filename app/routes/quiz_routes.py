from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.permissions import IsCompanyOwnerOrAdmin
from app.db.database import get_session
from app.schemas import quiz_schemas as schemas
from app.services.quiz_service import QuizService

router = APIRouter()


@router.get('/companies/{company_id}/quizzes', response_model=schemas.QuizListResponse)
async def get_company_quizzes(
		company_id: int,
		db: AsyncSession = Depends(get_session)
):
	service = QuizService(db)
	return {'quizzes': await service.get_quizzes(company_id)}


@router.post('/companies/{company_id}/quizzes/create', response_model=schemas.Quiz)
async def create_quiz(
		company_id: int,
		quiz: schemas.QuizCreate,
		token: str = Depends(settings.oauth2_scheme),
		db: AsyncSession = Depends(get_session)
):
	service = QuizService(db)
	await IsCompanyOwnerOrAdmin(db=db, token=token, company_id=company_id).__call__()
	return await service.create_quiz(company_id=company_id, quiz=quiz, token=token)


@router.put('/companies/{company_id}/quizzes/{quiz_id}', response_model=schemas.Quiz)
async def update_quiz(
		company_id: int,
		quiz_id: int,
		quiz: schemas.QuizUpdate,
		token: str = Depends(settings.oauth2_scheme),
		db: AsyncSession = Depends(get_session)
):
	service = QuizService(db)
	await IsCompanyOwnerOrAdmin(db=db, token=token, company_id=company_id).__call__()
	return await service.update_quiz(quiz=quiz, quiz_id=quiz_id, token=token)


@router.delete('/companies/{company_id}/quizzes/{quiz_id}')
async def delete_quiz(
		company_id: int,
		quiz_id: int,
		token: str = Depends(settings.oauth2_scheme),
		db: AsyncSession = Depends(get_session)
):
	service = QuizService(db)
	await IsCompanyOwnerOrAdmin(db=db, token=token, company_id=company_id).__call__()
	return await service.delete_quiz(quiz_id=quiz_id)

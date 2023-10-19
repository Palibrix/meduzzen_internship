from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.exceptions import ObjectNotFound
from app.models.quiz_model import Quiz, Question
from app.schemas.quiz_schemas import QuizCreate
from app.schemas import quiz_schemas as schemas
from app.services.user_service import UserService


class QuizService:

	def __init__(self, db):
		self.db = db

	async def get_quizzes(self, company_id):
		statement = select(Quiz).where(Quiz.quiz_company_id == company_id).options(selectinload(Quiz.questions))
		result = await self.db.execute(statement)
		return result.scalars().all()

	async def get_one_quiz_result(self, quiz_id):
		statement = select(Quiz).where(Quiz.quiz_id == quiz_id)
		result = await self.db.execute(statement)
		return result.scalars().first()

	async def get_one_quiz(self, quiz_id):
		quiz = await self.get_one_quiz_result(quiz_id=quiz_id)

		if quiz is None:
			raise ObjectNotFound

		return quiz

	async def create_quiz(self, company_id, quiz, token):
		user_service = UserService(self.db)
		active_user = await user_service.get_current_user(token=token)

		quiz_dict = quiz.model_dump()
		quiz_dict['quiz_company_id'] = company_id
		quiz_dict['created_by'] = active_user.user_id
		quiz_dict['updated_by'] = active_user.user_id
		quiz_dict['questions'] = [Question(**question) for question in quiz_dict['questions']]
		new_quiz = Quiz(**quiz_dict)

		self.db.add(new_quiz)
		await self.db.commit()
		await self.db.refresh(new_quiz)
		return new_quiz

	async def update_quiz(self, quiz, quiz_id, token):
		user_service = UserService(self.db)
		active_user = await user_service.get_current_user(token=token)

		db_quiz = await self.get_one_quiz(quiz_id=quiz_id)
		for key, value in quiz.model_dump(exclude_none=True).items():
			setattr(db_quiz, key, value)
		db_quiz.updated_by = active_user.user_id
		await self.db.commit()
		return db_quiz

	async def delete_quiz(self, quiz_id):
		db_quiz = await self.get_one_quiz(quiz_id=quiz_id)
		await self.db.delete(db_quiz)
		await self.db.commit()
		return {"detail": "Quiz deleted"}

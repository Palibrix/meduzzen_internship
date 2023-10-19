from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, ARRAY
from sqlalchemy.orm import relationship

from app.db.database import Base


class Quiz(Base):
    __tablename__ = 'quizzes'

    quiz_id = Column(Integer, primary_key=True, index=True, nullable=False)
    quiz_name = Column(String(30), nullable=False)
    quiz_title = Column(String(30), nullable=False)
    quiz_description = Column(String(70), nullable=False)
    quiz_frequency = Column(Integer)
    quiz_company_id = Column(Integer, ForeignKey('companies.company_id'))

    questions = relationship("Question", back_populates="quiz", lazy='selectin')

    created_by = Column(Integer, ForeignKey('users.user_id'))
    updated_by = Column(Integer, ForeignKey('users.user_id'))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    answer_options = Column(ARRAY(String), nullable=False)
    correct_answer = Column(Integer, nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"))

    quiz = relationship("Quiz", back_populates="questions")

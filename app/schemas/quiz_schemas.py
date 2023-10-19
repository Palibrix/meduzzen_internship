from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class QuestionBase(BaseModel):
    question_text: str
    answer_options: List[str] = Field(..., min_items=2)
    correct_answer: int


class QuizBase(BaseModel):

    quiz_name: str
    quiz_title: str
    quiz_description: str
    quiz_frequency: int
    questions: List[QuestionBase] = Field(..., min_items=2)


class QuizCreate(QuizBase):
    pass


class QuestionUpdate(BaseModel):
    question_id: int
    question_text: Optional[str] = None
    answer_options: Optional[List[str]] = None
    correct_answer: Optional[int] = None


class QuizUpdate(BaseModel):
    quiz_name: Optional[str] = None
    quiz_title: Optional[str] = None
    quiz_description: Optional[str] = None
    quiz_frequency: Optional[int] = None
    # questions: Optional[List[QuestionUpdate]] = None


class Quiz(QuizBase):
    quiz_company_id: int
    quiz_id: int

    created_by: int
    updated_by: int


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    pass


class QuizListResponse(BaseModel):
    quizzes: List[Quiz]

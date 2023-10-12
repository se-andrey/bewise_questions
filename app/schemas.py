from datetime import datetime

from fastapi import Header
from pydantic import BaseModel, Field

from .models import Question


class QuestionCreate(BaseModel):
    question_id: int
    question_text: str
    question_text_answer: str
    question_date_created: datetime

    class Config:
        from_attributes = True


class QuestionRequest(BaseModel):
    questions_number: int = Field(..., gt=0)


def get_questions_numbers(
        number: int = Header(..., alias="questions-numbers")
):
    return QuestionRequest(questions_number=number)


def get_question_entity(question: QuestionCreate) -> Question:
    return Question(
        question_id=question.question_id,
        question_text=question.question_text,
        question_text_answer=question.question_text_answer,
        question_date_created=question.question_date_created,
    )

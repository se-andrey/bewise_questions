from sqlalchemy import Column, DateTime, Integer, Text

from .database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    question_text = Column(Text)
    question_text_answer = Column(Text)
    question_date_created = Column(DateTime)

import datetime

import requests
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import desc

from .database import close_db, get_session, init_db
from .logger import logger
from .models import Question
from .schemas import (QuestionCreate, QuestionRequest, get_question_entity,
                      get_questions_numbers)

app = FastAPI()

app.add_event_handler("startup", init_db)
app.add_event_handler("shutdown", close_db)


@app.post("/questions")
def get_questions(
        request: QuestionRequest = Depends(get_questions_numbers),
        db=Depends(get_session)
):
    last_question = db.query(Question).order_by(desc(Question.id)).first()

    questions = api_questions(request.questions_number)
    for question in questions:

        question_created_date = datetime.datetime.fromisoformat(question['created_at'])
        question_data = get_question_entity(QuestionCreate(
            question_id=question['id'],
            question_text=question['question'],
            question_text_answer=question['answer'],
            question_date_created=question_created_date,
        ))

        db.add(question_data)

    logger.info(f"New {request.questions_number} question(s) added to the database")

    db.commit()
    if last_question:
        db.refresh(last_question)

    else:
        last_question = {}

    return last_question


def api_questions(quantity: int):
    url = f"https://jservice.io/api/random?count={quantity}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            logger.error("Failed to fetch questions from the API")
            raise HTTPException(status_code=500, detail="Failed to fetch questions from the API")

    except requests.Timeout:
        logger.error("Gateway timeout")
        raise HTTPException(status_code=504, detail="Gateway timeout")

    return response.json()

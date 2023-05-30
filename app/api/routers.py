from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_async_session


router = APIRouter(prefix="/download", tags=["Audio"])


@router.post(
    "/",
    status_code=HTTPStatus.OK,
    response_model_exclude_none=True,
    summary="Get questions"
)
async def get_questions(
        request: QuestionsRequest,
        session: AsyncSession = Depends(get_async_session)
) -> List[QuestionResponse]:
    result = await question_service.get_and_save_questions(request.questions_num, session)
    return result

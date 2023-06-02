from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import RecordResponse, UserCreateRequest, UserResponse
from app.core.db.db import get_async_session
from app.services.media_services import media_service
from app.services.user_services import user_service


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post(
    "/upload",
    status_code=HTTPStatus.CREATED,
    tags=["Upload"],
    summary="Upload wav file to server."
)
async def upload_media(
        file: UploadFile,
        token: UUID = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_async_session)
) -> RecordResponse:
    return await media_service.upload_media(file, token, session)


@router.post(
    "/users",
    status_code=HTTPStatus.CREATED,
    tags=["User"],
    summary="Create new user."
)
async def create_user(
        user_data: UserCreateRequest,
        session: AsyncSession = Depends(get_async_session)
) -> UserResponse:
    """Create a new user.
    - **username**: unique username
    """
    user = await user_service.create_user(user_data, session)
    return UserResponse(username=user.username, token=user.token)

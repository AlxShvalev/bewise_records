import os
from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException, UploadFile
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import RecordResponse
from app.core.db.models import Record
from app.core.config import BASE_DIR, settings
from app.services.user_services import user_service


def get_full_download_url(user_id: int, record_id: int):
    return f"http://{settings.host}:{settings.ip_port}/record?id={record_id}&user={user_id}"


class MediaService:

    async def upload_record(
            self,
            file: UploadFile,
            token: UUID,
            session: AsyncSession
    ):
        """Uploads media file to server and saves into database."""
        user = await user_service.get_or_404(token, session)
        user_id = user.id
        path = await self._save_file(file, user.id)
        media = Record(
            title=file.filename,
            file_url=path,
            owner_id=user_id
        )
        media = await self._save_to_db(media, session)
        download_url = get_full_download_url(user_id, media.id)
        return RecordResponse(download_url=download_url)

    async def download_record(self, record_id: int, user_id: int, session: AsyncSession):
        """Gets related file path from the database and returns full file path."""
        file_path = await self._get_record_path(record_id, user_id, session)
        return os.path.join(BASE_DIR, file_path)

    async def _get_record_path(self, record_id: int, user_id: int, session: AsyncSession):
        """Gets record from the database by record id and owner id."""
        statement = select(Record.file_url).where(and_(Record.id == record_id, Record.owner_id == user_id))
        record = await session.execute(statement)
        file_path = record.scalars().first()
        if file_path:
            return file_path
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Record with id={record_id} and owner id={user_id} is not found"
        )

    async def _save_file(self, file: UploadFile, user_id: int) -> str:
        db_path = os.path.join(settings.media_dir, str(user_id))
        root_path = os.path.join(BASE_DIR, db_path)
        if not os.path.exists(root_path):
            os.mkdir(root_path)
        if os.path.exists(os.path.join(root_path, file.filename)):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="File already exists"
            )
        os.chdir(root_path)
        content = await file.read()
        with open(file.filename, mode="wb") as f:
            f.write(content)
        return os.path.join(db_path, file.filename)

    async def _save_to_db(self, file: Record, session: AsyncSession) -> Record:
        session.add(file)
        await session.commit()
        await session.refresh(file)
        return file


media_service = MediaService()

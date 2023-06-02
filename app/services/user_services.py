from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import UserCreateRequest
from app.core.db.models import User


class UserService:

    async def _get_by_token(
            self,
            token: UUID,
            session: AsyncSession
    ) -> Optional[User]:
        token = self._validate_token(token)
        statement = select(User).where(User.token == token)
        user = await session.execute(statement)
        return user.scalars().first()

    async def _get_by_username(
            self,
            username: str,
            session: AsyncSession
    ) -> Optional[User]:
        """Get user by username"""
        statement = select(User).where(User.username == username)
        user = await session.execute(statement)
        return user.first()

    def _validate_token(self, token):
        try:
            UUID(token, version=4)
            return token
        except ValueError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="User is not authorized or entered invalid token"
            )

    async def create_user(
            self,
            user_data: UserCreateRequest,
            session: AsyncSession
    ) -> User:
        """Write user into the database."""
        user = User(username=user_data.username)
        user_from_db = await self._get_by_username(
            username=user_data.username,
            session=session
        )
        if user_from_db:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="User already exists"
            )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_or_404(self, token: UUID, session: AsyncSession) -> User:
        """Get user by token, raises NOT_FOUND error, if user is not exists."""
        user = await self._get_by_token(token, session)
        if user:
            return user
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")


user_service = UserService()

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import UserCreateRequest
from app.core.db.models import User
from app.exceptions import AlreadyExistsException, NotFoundException, UnauthorizedException


class UserService:

    async def _get_by_token(
            self,
            token: UUID,
            session: AsyncSession
    ) -> Optional[User]:
        """Get user by token."""
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
            raise UnauthorizedException

    async def create_user(
            self,
            user_data: UserCreateRequest,
            session: AsyncSession
    ) -> User:
        """Save user into the database."""
        user = User(username=user_data.username)
        user_from_db = await self._get_by_username(
            username=user_data.username,
            session=session
        )
        if user_from_db:
            raise AlreadyExistsException("User", username=user_data.username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_or_404(self, token: UUID, session: AsyncSession) -> User:
        """Get user by token, raises NOT_FOUND error, if user is not exists."""
        user = await self._get_by_token(token, session)
        if user:
            return user
        raise NotFoundException("User", token=token)


user_service = UserService()

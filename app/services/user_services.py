from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import UserCreateRequest
from app.core.db.models import User


class UserService:
    async def create_user(
            self,
            user_data: UserCreateRequest,
            session: AsyncSession
    ):
        user = User(username=user_data.username)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


user_service = UserService()

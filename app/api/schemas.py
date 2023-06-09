from uuid import UUID

from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=255)

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    username: str
    token: UUID


class RecordResponse(BaseModel):
    download_url: str

import uuid
from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    String,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr, relationship
from sqlalchemy.schema import ForeignKey


@as_declarative()
class Base:
    """Base model."""
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
        onupdate=func.current_timestamp()
    )

    __name__: str


class User(Base):
    """User model"""
    username = Column(String(255), nullable=False, unique=True)
    token = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4())
    files = relationship("File", back_populates="owner")


class File(Base):
    file_url = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey(User.id), nullable=False)
    owner = relationship("User", back_populates="files")

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from .engine import Base

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    fullname: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    address: Mapped[Optional[str]] = mapped_column(String(200))
    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
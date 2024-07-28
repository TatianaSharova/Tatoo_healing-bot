from typing import Optional

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    '''Модель для пользователя.'''
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    healing_method: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    notify_counter: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

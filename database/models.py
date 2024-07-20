from typing import Optional

from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    '''Модель для пользователя.'''
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    user_id: Mapped[str] = mapped_column(Integer, nullable=False)
    healing_method: Mapped[str] = mapped_column(String(8))
    notify_counter: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

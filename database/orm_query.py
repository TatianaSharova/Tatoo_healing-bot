from aiogram import types
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def orm_user(session: AsyncSession,
                               data: dict, message: types.Message):
    '''Создание подписки на уведомления.'''
    obj = User(
        user_id=message.from_user.id,
        healing_method=data['healing_method']
        )
    session.add(obj)
    await session.commit()


async def orm_get_list_users(session: AsyncSession):
    '''Получить абсолютно все подписки, для админа.'''
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_user(session: AsyncSession, user_id: int):
    '''Удалить пользователя из базы данных.'''
    query = delete(User).where(User.user_id == user_id)
    await session.execute(query)
    await session.commit()

from aiogram import types
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Data


async def orm_get_list_users(session: AsyncSession):
    '''Получить абсолютно все подписки, для админа.'''
    query = select(Data)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_user(session: AsyncSession, user_id: int):
    '''Удалить пользователя из базы данных.'''
    query = delete(Data).where(Data.user_id == user_id)
    await session.execute(query)
    await session.commit()

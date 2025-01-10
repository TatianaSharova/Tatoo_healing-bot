from aiogram import types
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def orm_add_user(session: AsyncSession,
                       message: types.Message):
    '''Добавление пользователя в базу данных.'''
    obj = User(
        user_id=message.from_user.id,
        username=message.from_user.username
        )
    session.add(obj)
    await session.commit()


async def orm_get_user(session: AsyncSession, user_id: int):
    '''Получить определенную подписку пользователя.'''
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_add_healing_method(session: AsyncSession,
                                 message: types.Message):
    '''Добавление пользователя в базу данных.'''
    user = await orm_get_user(session, message.from_user.id)
    user.healing_method = message.text
    session.add(user)
    await session.commit()


async def orm_get_list_users(session: AsyncSession):
    '''Получить все подписки.'''
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_user(session: AsyncSession, user_id: int):
    '''Удалить пользователя из базы данных.'''
    query = delete(User).where(User.user_id == user_id)
    await session.execute(query)
    await session.commit()

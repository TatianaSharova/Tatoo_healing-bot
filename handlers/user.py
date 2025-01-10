import asyncio

from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandStart
from apscheduler.jobstores.base import JobLookupError
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import (orm_add_healing_method, orm_add_user,
                                orm_get_user)
from keyboards import reply
from scheduler.scheduler import (scheduler, send_instr_for_compress,
                                 send_instr_for_skin)
from texts import COMPRESS_END

user_canal_router = Router()


@user_canal_router.message(CommandStart())
async def send_welcome(message: types.Message,
                       session: AsyncSession) -> None:
    '''
    Присылает пользователю приветственное сообщение.
    Если пользователь новый, предлагает выбрать способ заживления.
    '''
    user = await orm_get_user(session, message.from_user.id)
    if user:
        await message.answer(
            'Рад снова с тобой увидеться!'
        )
    else:
        await orm_add_user(session, message)
        await message.answer(
            'Привет! Давай заживим твоё тату!'
        )
        await message.answer(
            'Выбери способ заживления:',
            reply_markup=reply.start_kb
        )


@user_canal_router.message(Command('help'))
@user_canal_router.message(F.text.lower() == 'помощь')
async def get_help(message: types.Message) -> None:
    '''
    Присыдает пользователю сообщение с инфорацией о своей работе.
    '''
    await message.answer(
        'Я помогу тебе правильно заживить твое тату!.',
        parse_mode=ParseMode.HTML,
        )


@user_canal_router.message(F.text.strip().lower() == 'плёнка')
async def choose_skin(message: types.Message,
                      session: AsyncSession) -> None:
    '''
    Заносит данные о выбранном методе в базу данных и
    присылает пользователю информационное сообщение о его выборе.
    '''
    await orm_add_healing_method(session, message)
    await message.answer(
        'Ты заживляешь тату с помощью пленки, супер! '
        'Буду каждый день слать тебе сообщение '
        'с инструкцией по уходу.',
        parse_mode=ParseMode.HTML,
        )
    asyncio.create_task(send_instr_for_skin(message))


@user_canal_router.message(F.text.strip().lower() == 'компресс')
async def choose_compress(message: types.Message,
                          session: AsyncSession) -> None:
    '''
    Заносит данные о выбранном методе в базу данных и
    присылает пользователю информационное сообщение о его выборе.
    '''
    await orm_add_healing_method(session, message)
    await message.answer(
        'Ты заживляешь тату с помощью компресса, супер! '
        'Буду каждый день слать тебе 3 сообщения '
        'с инструкциями по уходу.',
        parse_mode=ParseMode.HTML,
        )
    asyncio.create_task(send_instr_for_compress(message))


@user_canal_router.callback_query(F.data.startswith('healed_'))
async def stop_sending_instructions(callback: types.CallbackQuery):
    '''Удаляет задачи по рассылке инструкций по уходу.'''
    user_id = callback.data.split('_')[-1]
    try:
        for job_id in [
            f'note_morning_{user_id}',
            f'note_lunch_{user_id}',
            f'note_evening_{user_id}'
        ]:
            scheduler.remove_job(job_id)
    except JobLookupError:
        pass
    await callback.answer()
    await callback.message.answer(f'{COMPRESS_END}')


@user_canal_router.callback_query(F.data.startswith('not_healed_'))
async def continue_sending_instructions(callback: types.CallbackQuery):
    '''
    Продолжает рассылку уведомлений по уходу.
    '''
    user_id = callback.data.split('_')[-1]
    await callback.answer()
    await callback.message.answer('Хорошо! Продолжаю присылать напоминания.')
    try:
        for job_id in [
            f'note_morning_{user_id}',
            f'note_lunch_{user_id}',
            f'note_evening_{user_id}'
        ]:
            scheduler.remove_job(job_id)
    except JobLookupError:
        pass
    asyncio.create_task(send_instr_for_compress(callback.message))

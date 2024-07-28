from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandStart
from database.orm_query import orm_get_user, orm_add_user, orm_add_healing_method
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import reply


user_canal_router = Router()


@user_canal_router.message(CommandStart())
async def send_welcome(message: types.Message,
                       session: AsyncSession) -> types.Message:
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
        reply_markup=reply.start_kb)


@user_canal_router.message(Command('help'))
@user_canal_router.message(F.text.lower() == 'помощь')
async def get_help(message: types.Message) -> types.Message:
    await message.answer(
        'я бот, помогающий тебе заживить тату.',
        parse_mode=ParseMode.HTML,
        )


@user_canal_router.message(F.text.strip().lower() == 'плёнка')
async def choose_skin(message: types.Message, session: AsyncSession):
    await orm_add_healing_method(session, message)
    await message.answer(
        'Ты заживляешь тату с помощью пленки, супер! Буду каждый день слать тебе сообщение.',
        parse_mode=ParseMode.HTML,
        )




@user_canal_router.message(F.text.strip().lower() == 'компресс')
async def choose_compress(message: types.Message, session: AsyncSession):
    await orm_add_healing_method(session, message)
    await message.answer(
        'Ты заживляешь тату с помощью компресса, супер! Буду каждый день слать тебе 3 сообщения.',
        parse_mode=ParseMode.HTML,
        )

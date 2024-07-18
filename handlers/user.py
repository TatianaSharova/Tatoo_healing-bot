from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandStart

from keyboards import reply


user_canal_router = Router()


@user_canal_router.message(CommandStart())
async def send_welcome(message: types.Message) -> types.Message:
    await message.answer(
        'Привет! Давай заживим твоё тату!',
        parse_mode=ParseMode.HTML
        )

    await message.answer(
        'Выбери способ заживления',
        parse_mode=ParseMode.HTML,
        reply_markup=reply.start_kb)


@user_canal_router.message(Command('help'))
@user_canal_router.message(F.text.lower() == 'помощь')
async def get_help(message: types.Message) -> types.Message:
    await message.answer(
        'я бот, помогающий тебе заживить тату.',
        parse_mode=ParseMode.HTML,
        )

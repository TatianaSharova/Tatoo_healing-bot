from aiogram import F, Router, types
from filters.chat_types import IsAdmin
from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandStart


admin_router = Router()
admin_router.message.filter(IsAdmin())

@admin_router.message(Command('admin'))
@admin_router.message(F.text.lower() == 'admin')
async def get_help(message: types.Message) -> types.Message:
    await message.answer(
        'админка',
        parse_mode=ParseMode.HTML,
        )
import os

from aiogram import Bot, types
from aiogram.filters import Filter
from dotenv import load_dotenv

load_dotenv()


ADMIN = int(os.getenv('ADMIN'))
ADMIN_2 = int(os.getenv('ADMIN_2'))


class IsAdmin(Filter):
    '''Фильтр для доступа только админам.'''
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in [ADMIN, ADMIN_2]

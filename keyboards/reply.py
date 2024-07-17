from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Плёнка"),
            types.KeyboardButton(text="Компресс")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
    )

from aiogram import types

from keyboards.inline import get_callback_btns


async def send_one_time(message: types.Message, text) -> None:
    '''Отправляет сообщение с текстом.'''
    await message.answer(text)


async def send_question(message: types.Message,
                        user_id: str) -> None:
    '''Отправляет вопрос о состоянии татуировки.'''
    await message.answer(
        'Зажила ли татуировка?',
        reply_markup=get_callback_btns(
            btns={
                'Зажила': f'healed_{user_id}',
                'Не зажила': f'not_healed_{user_id}',
            }))

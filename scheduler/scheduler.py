from datetime import datetime, timedelta

from aiogram import types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from texts import COMPRESS_1, SKIN_1, SKIN_2, SKIN_END

from .messages import send_one_time, send_question

scheduler = AsyncIOScheduler(timezone='Asia/Dubai')


async def create_new_question_task(
        message: types.Message,
        user_id: str) -> None:
    '''
    Создает новую задачу для apscheduler:
    - Присылает через день в 9 утра вопрос о том, зажила ли татуировка.
    '''
    question = scheduler.add_job(
        send_question, 'date',
        id=f'question_{user_id}',
        next_run_time=datetime.now() + timedelta(
            days=2, hours=9-datetime.now().hour,
            minutes=60-datetime.now().minute),
        kwargs={'message': message, 'user_id': user_id}
    )


async def send_instr_for_skin(message: types.Message) -> None:
    '''Создает 3 задачи для apscheduler:
    - Написать в 11:00 следующего дня с инструкцией SKIN_1.
    - Написать в 11:00 через 1 день с инструкцией SKIN_2.
    - Написать в 11:00 через 2 дня с инструкцией SKIN_END.'''
    first_not = scheduler.add_job(
        send_one_time, trigger='date',
        next_run_time=datetime.now() + timedelta(
            days=1, hours=11-datetime.now().hour,
            minutes=60-datetime.now().minute),
        kwargs={'message': message, 'text': SKIN_1})

    second_not = scheduler.add_job(
        send_one_time, trigger='date',
        next_run_time=datetime.now() + timedelta(
            days=2, hours=11-datetime.now().hour,
            minutes=60-datetime.now().minute),
        kwargs={'message': message, 'text': SKIN_2})

    end_not = scheduler.add_job(
        send_one_time, trigger='date',
        next_run_time=datetime.now() + timedelta(
            days=2, hours=11-datetime.now().hour,
            minutes=60-datetime.now().minute),
        kwargs={'message': message, 'text': SKIN_END})


async def send_instr_for_compress(
        message: types.Message) -> None:
    '''
    3 раза в день отправляет инструкцию-напоминание и смене компресса.
    На второй день присылает вопрос о том, зажила ли татуировка.
    '''
    user_id = message.from_user.id

    first_not = scheduler.add_job(
        send_one_time, trigger='cron',
        id=f'note_morning_{user_id}',
        hour=11, minute=0,
        kwargs={'message': message, 'text': COMPRESS_1})

    second_not = scheduler.add_job(
        send_one_time, trigger='cron',
        id=f'note_lunch_{user_id}',
        hour=15, minute=0,
        kwargs={'message': message, 'text': COMPRESS_1})

    third_not = scheduler.add_job(
        send_one_time, trigger='cron',
        id=f'note_evening_{user_id}',
        hour=20, minute=0,
        kwargs={'message': message, 'text': COMPRESS_1})

    question = await create_new_question_task(message, user_id)

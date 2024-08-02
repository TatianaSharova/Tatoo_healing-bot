from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime
from aiogram import types, Bot
from texts import SKIN_1, SKIN_2, SKIN_END

scheduler = AsyncIOScheduler(timezone='Asia/Dubai')


async def send_one_time(message: types.Message, text):
    await message.answer(text)

async def send_instr_for_skin(message: types.Message):
    scheduler.add_job(
        send_one_time(), trigger='date',
        next_run_time=datetime.now() + timedelta(
            days=1, hours=11-datetime.now().hour,
            minutes=60-datetime.now().minute),
        kwargs={'message' : message, 'text' : SKIN_1})
    
    scheduler.add_job(
        send_one_time(), trigger='date',
        next_run_time=datetime.now() + timedelta(
            days=2, hours=11-datetime.now().hour,
            minutes=60-datetime.now().minute),
        kwargs={'message' : message, 'text' : SKIN_2})
    
    scheduler.add_job(
        send_one_time(), trigger='date',
        next_run_time=datetime.now() + timedelta(
            days=2, hours=11-datetime.now().hour,
            minutes=60-datetime.now().minute),
        kwargs={'message' : message, 'text' : SKIN_END})











async def send_time(bot: Bot):
    await bot.send_message(589097349,'now')

async def send_cron(bot: Bot):
    await bot.send_message(589097349,'every day')

async def send_interval(bot: Bot):
    await bot.send_message(589097349,'every min')

# scheduler.add_job(send_time, trigger='date', next_run_time=datetime.now()+timedelta(seconds=5),
#                   kwargs={'bot' : bot})


# # scheduler.add_job(send_cron, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute+1,
# #                   start
# #                   kwargs={'bot' : bot})

# send_interval_job = scheduler.add_job(send_interval, 'interval', minutes=1, args=(bot,))
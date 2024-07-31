import asyncio
import logging
import os
from pytz import utc
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from database.engine import create_db, drop_db, session_maker
from handlers.user import user_canal_router
from handlers.admin import admin_router
from keyboards.bot_cmds_list import bot_cmds
from middlewares.media import MediaMiddleware
from middlewares.db import DataBaseSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


# jobstores = {
#     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
# }
# executors = {
#     'default': ThreadPoolExecutor(20),
#     'processpool': ProcessPoolExecutor(5)
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 3
# }
scheduler = AsyncIOScheduler(timezone='Asia/Dubai')

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')


logging.basicConfig(level=logging.INFO)


dp: Dispatcher = Dispatcher()
bot: Bot = Bot(token=TELEGRAM_TOKEN)
#scheduler = AsyncIOScheduler(timezone='Europe/Samara')
#scheduler.configure(timezone=)
dp.include_router(admin_router)
dp.include_router(user_canal_router)


async def send_time(bot: Bot):
    await bot.send_message(589097349,'now')

async def send_cron(bot: Bot):
    await bot.send_message(589097349,'every day')

async def send_interval(bot: Bot):
    await bot.send_message(589097349,'every min')

scheduler.add_job(send_time, trigger='date', next_run_time=datetime.now()+timedelta(seconds=5),
                  kwargs={'bot' : bot})


# scheduler.add_job(send_cron, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute+1,
#                   start
#                   kwargs={'bot' : bot})

send_interval_job = scheduler.add_job(send_interval, 'interval', minutes=1, args=(bot,))




async def on_startup(bot):
    '''Запускает БД.'''

    run_param = True
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('Бот выключен.')


async def main():
    '''Запуск бота.'''
    dp.message.middleware(MediaMiddleware())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)

    # await bot.set_my_commands(commands=bot_cmds,
    #                           scope=types.BotCommandScopeAllPrivateChats())

    while True:
        scheduler.start()
        await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

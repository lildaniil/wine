from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

from utils.db_api import db_gino
from utils.db_api import commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    # Creating DB
    print("Creating database")
    await db_gino.on_startup(dp)
    print("Done!")

    # Creating tables in DB
    print("Creating tables")
    await db.gino.create_all()
    print("Done!")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)


from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("add_wine", "Добавить вино"),
            types.BotCommand("search", "Найти, что пил (если не помнишь)"),
            
        ]
    )

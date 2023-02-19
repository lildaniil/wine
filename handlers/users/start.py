from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, channel_log_id

from utils.db_api import commands
from utils.stat.set_stats import set_stat_data


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    # add user into db 
    if await commands.select_user(message.from_user.id) == None:
        print("New user")
        await commands.add_user(
            id = message.from_user.id,
            first_name = message.from_user.first_name,
            last_name = message.from_user.last_name,
            username = message.from_user.username,
            language_code = message.from_user.language_code,
            is_bot = message.from_user.is_bot,
            is_premium = message.from_user.is_premium,
            added_to_attachment_menu = message.from_user.added_to_attachment_menu,
            can_join_groups = message.from_user.can_join_groups,
            can_read_all_group_messages = message.from_user.can_read_all_group_messages,
            supports_inline_queries = message.from_user.supports_inline_queries
            )

        # sent to log chat
        await message.bot.send_message(channel_log_id, f"""
#wine\n
new user:\n\n
id: {message.from_user.id}\n
username: {message.from_user.username}\n
name: {message.from_user.first_name} {message.from_user.last_name}\n
""")

    #     await set_stat_data(
    #         user_id=message.from_user.id,
    #         action='start',
    #         action_data='new user'
    #         )
    # else: await set_stat_data(
    #         user_id=message.from_user.id,
    #         action='start'
    #         )



    await message.answer(f"""
Привет, {message.from_user.full_name}!\n
Это винный бот \n
Что может этот бот?\n
Ничего!
""")

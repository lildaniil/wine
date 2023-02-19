from aiogram import types

from loader import dp
from utils.db_api import commands

async def set_stat_data(
    user_id:int,
    action:str,
    action_data:str = None
    ):

    await commands.add_stat(
        user_id=user_id,
        action=action,
        action_data=action_data
    )    
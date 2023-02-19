from asyncpg import UniqueViolationError
import asyncpg

from utils.db_api.schema.user import User
from utils.db_api.schema.stat import Statistic
from utils.db_api.schema.wine import Wine
from utils.db_api.schema.barcode import Barcode
from utils.db_api.db_gino import db

import logging


# 
# USER COMMANDS
# 

async def add_user(
    id:int,
    first_name:str, 
    last_name:str, 
    username:str,
    language_code:str,
    is_bot:str,
    is_premium:bool,
    added_to_attachment_menu:bool,
    can_join_groups:bool,
    can_read_all_group_messages:bool,
    supports_inline_queries:bool
    ):
    
    try:
        user = User(
            id=id, 
            first_name=first_name, 
            last_name=last_name, 
            username=username,
            language_code=language_code,
            is_bot = is_bot,
            is_premium=is_premium,
            added_to_attachment_menu=added_to_attachment_menu,
            can_join_groups=can_join_groups,
            can_read_all_group_messages=can_read_all_group_messages,
            supports_inline_queries=supports_inline_queries
            )

        await user.create()

    except UniqueViolationError:
        pass


async def select_all_users():

    users = await User.query.gino.all()
    return users


async def select_user(id:int):
    
    user = await User.query.where(User.id == id).gino.first()

    return user


async def count_users():

    total = await db.func.count(User.id).gino.scalar()


async def update_user_username(id, username):
    
    user = await User.get(id)

    await user.update(username=username).apply()


# 
# WINE COMMANDS
# 

async def add_wine(
    created_by:int,
    image:str,
    wine:str,
    score:float,
    grape:str,
    sugar:int,
    color:int,
    country:str,
    producer:str,
    year:int,
    location:str,
    price:float,
    comment:str
    ):
    
    try:
        wine = Wine(
            created_by=created_by,
            image=image,
            wine=wine,
            grape=grape,
            score=score,
            sugar=sugar,
            color=color,
            country=country,
            producer=producer,
            year=year,
            location=location,
            price=price,
            comment=comment
            )

        await wine.create()

    except UniqueViolationError:
        pass


async def select_all_wines():

    wines = await Wine.query.gino.all()
    return wines


async def select_wine_by_name(wine_name:str, user_id:int=0):
    if user_id != 0: 
        wines = await Wine.query.where(
            (Wine.wine.op('LIKE')(f'%{wine_name}%'))&(Wine.created_by == user_id)
            ).gino.all()
    else:
        wines = await Wine.query.where(Wine.wine.op('LIKE')(f'%{wine_name}%')).gino.all()
    return wines


async def select_wine_by_color(wine_color:int, user_id:int=0):
    if user_id != 0:       
        wines = await Wine.query.where(
                (Wine.color == wine_color) & (Wine.created_by == user_id)
            ).gino.all()
    else:
        wines = await Wine.query.where(Wine.color == wine_color).gino.all()
    return wines


async def select_wine_by_sugar(wine_sugar:int, user_id:int=0):
    if user_id != 0:
        wines = await Wine.query.where(
            (Wine.sugar == wine_sugar)&(Wine.created_by == user_id)
            ).gino.all()
    else:
        wines = await Wine.query.where(Wine.sugar == wine_sugar)
    return wines


async def select_wine(id:int):
    
    wine = await User.query.where(User.id == id).gino.first()

    return wine


async def count_wines():

    total = await db.func.count(User.id).gino.scalar()

    return total




# 
# STATISTIC COMMANDS
# 


async def add_stat(
    # id:int,
    user_id:int,
    action:str,
    action_data:str = None
    ):

    try:
        stat = Statistic(
            user_id=user_id,
            action=action,
            action_data=action_data
        )

        await stat.create()

    except UniqueViolationError:
        pass


# 
# BARCODE COMMANDS
# 


async def add_barcode(
    created_by:int,
    bc_image:str,
    bc_number:str,
    type:float,
    wine_image:str,
    ):
    
    try:
        barcode = Barcode(
            created_by=created_by,
            bc_image=bc_image,
            bc_number=bc_number,
            type=type,
            wine_image=wine_image
            )

        await barcode.create()

    except UniqueViolationError:
        pass

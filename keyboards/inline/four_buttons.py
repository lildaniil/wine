from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_factory import four_query


def create_four_button(texts:dict, query=four_query):

    four_keyboard = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text=texts.get(1),
                callback_data=query.new(num='1')
                ),
                InlineKeyboardButton(text=texts.get(2),
                callback_data=query.new(num='2')
                )
            ],
            [
                InlineKeyboardButton(text=texts.get(3),
                callback_data=query.new(num='3')
                ),
                InlineKeyboardButton(text=texts.get(4),
                callback_data=query.new(num='4')
                )
            ]
        ]
    )

    return four_keyboard
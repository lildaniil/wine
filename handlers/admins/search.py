from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, channel_log_id

from utils.db_api import commands
from utils.stat.set_stats import set_stat_data

from filters import IsAdmin

from keyboards.inline.four_buttons import create_four_button
from keyboards.inline.callback_factory import search_query

from data.wine_dict import sugar_dict, color_dict, search_options

from states import WineSearchStateAdmin


# 
#    ___       SEARCH WINE     ___
# 



# requesting search options
@dp.message_handler(IsAdmin(), text = '/search_all')
async def search_wine(message: types.Message, state: FSMContext):
    await WineSearchStateAdmin.search.set()
    await message.answer("Как будем искать твое вено??", reply_markup=create_four_button(search_options, search_query))

    # sent to log chat
    await message.bot.send_message(channel_log_id, f"""
#wine - new search request
username: {message.from_user.username}\n""")


# 1 option - name
@dp.callback_query_handler(search_query.filter(num = '1'), state=WineSearchStateAdmin.search)
async def search_wine_by_name(call: types.CallbackQuery, state: FSMContext):

    await call.message.answer("Как зовут твое вено??")
    await WineSearchStateAdmin.serch_by_name.set()


# requesting search options - name
@dp.message_handler(state=WineSearchStateAdmin.serch_by_name)
async def search_wine_by_name_searching(message: types.Message, state: FSMContext):
    
    request = message.text.lower().strip()
    result = await commands.select_wine_by_name(wine_name=request)

    await message.answer(f'Найдено {len(result)} вена')

    for wine in result:
        text=f"""
{wine.wine}

Оценка: {wine.score}
Цена: {wine.price}

{sugar_dict.get(wine.sugar)}
{color_dict.get(wine.color)}

Виноград: {wine.grape}
Страна, производитель: {wine.country}, {wine.producer}
Год: {wine.year}
Где пилось: {wine.location}

Комментарий: {wine.comment}
"""
        await dp.bot.send_photo(
            message.from_user.id,
            photo=wine.image,
            caption=text
        )
    

    await state.finish()


# 2 option - sugar
@dp.callback_query_handler(search_query.filter(num = '2'), state=WineSearchStateAdmin.search)
async def search_wine_by_sugar(call: types.CallbackQuery, state: FSMContext):

    await call.message.answer("Выбирай", reply_markup=create_four_button(sugar_dict))
    await WineSearchStateAdmin.serch_by_sugar.set()


# requesting search options - sugar
@dp.callback_query_handler(state=WineSearchStateAdmin.serch_by_sugar)
async def search_wine_by_sugar_searching(call: types.CallbackQuery, state: FSMContext):
    

    request = int(call.data.split(':')[1])
    result = await commands.select_wine_by_sugar(wine_sugar=request)

    await call.message.answer(f'Найдено {len(result)} вена')

    for wine in result:
        text=f"""
{wine.wine}

Оценка: {wine.score}
Цена: {wine.price}

{sugar_dict.get(wine.sugar)}
{color_dict.get(wine.color)}

Виноград: {wine.grape}
Страна, производитель: {wine.country}, {wine.producer}
Год: {wine.year}
Где пилось: {wine.location}

Комментарий: {wine.comment}
"""
        await dp.bot.send_photo(
            call.message.chat.id,
            photo=wine.image,
            caption=text
        )
    

    await state.finish()




# 3 option - color
@dp.callback_query_handler(search_query.filter(num = '3'), state=WineSearchStateAdmin.search)
async def search_wine_by_color(call: types.CallbackQuery, state: FSMContext):

    await call.message.answer("Выбирай", reply_markup=create_four_button(color_dict))
    await WineSearchStateAdmin.serch_by_color.set()

# requesting search options - color
@dp.callback_query_handler(state=WineSearchStateAdmin.serch_by_color)
async def search_wine_by_color_searching(call: types.CallbackQuery, state: FSMContext):
    
    print(call.data)
    request = int(call.data.split(':')[1])
    result = await commands.select_wine_by_color(wine_color=request)

    await call.message.answer(f'Найдено {len(result)} вена')


    for wine in result:
        text=f"""
{wine.wine}

Оценка: {wine.score}
Цена: {wine.price}

{sugar_dict.get(wine.sugar)}
{color_dict.get(wine.color)}

Виноград: {wine.grape}
Страна, производитель: {wine.country}, {wine.producer}
Год: {wine.year}
Где пилось: {wine.location}

Комментарий: {wine.comment}
"""
        await dp.bot.send_photo(
            call.message.chat.id,
            photo=wine.image,
            caption=text
        )
    

    await state.finish()



# 4 option - memes
@dp.callback_query_handler(search_query.filter(num = '4'), state=WineSearchStateAdmin.search)
async def search_wine_by_name(call: types.Message, state: FSMContext):

    await call.message.answer("Как зовут твое вено??")
    await WineSearchStateAdmin.serch_by_name.set()
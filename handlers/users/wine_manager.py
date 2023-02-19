from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, channel_log_id

from utils.db_api import commands
from utils.stat.set_stats import set_stat_data

from filters import IsAdmin

from keyboards.inline.four_buttons import create_four_button
from keyboards.inline.callback_factory import search_query

from data.wine_dict import sugar_dict, color_dict, search_options

from states import WineAdderState, WineSearchState
import time 

start = ''


# 
#    ___       ADD NEW WINE     ___
# 


# requesting pic
@dp.message_handler(text = '/add_wine')
async def add_wine(message: types.Message):
    await WineAdderState.photo.set()
    await message.answer("Загрузи фото прикольдеса")

    global start 
    start = time.time() ## точка отсчета времени

    # sent to log chat
    await message.bot.send_message(channel_log_id, f"""
#wine - add new wine
username: {message.from_user.username}\n""")


# add pic
# requesting wine
@dp.message_handler(content_types=['photo'], state=WineAdderState.photo)
async def add_wine_set_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

        await message.answer("Как называется сие чуда?")
        await WineAdderState.next()

# add wine
# requesting score
@dp.message_handler(state=WineAdderState.wine)
async def add_wine_set_wine(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['wine'] = str(message.text)
        print(data['wine'])
    
        await message.answer("Теперь поставь оценку \n\nШкала от 0 до 10 \n0 - \"фу жесть как это попало в мой рот\" \n10 - Вау! Клас! Это не зря попало в мой рот")
        await WineAdderState.next()



# add score
# requesting grape
@dp.message_handler(state=WineAdderState.score)
async def add_wine_set_score(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['score'] = float(message.text)
        print(data['score'])
    
        await message.answer("Какой виноград?")
        await WineAdderState.next()


# add grape
# req sugar 
@dp.message_handler(state=WineAdderState.grape)
async def add_wine_set_grape(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['grape'] = message.text
        print(data['grape'])    
    
    await message.answer("По содержанию сахара:", reply_markup=create_four_button(sugar_dict)) 
    await WineAdderState.next()


# add sugar
# req color
@dp.callback_query_handler(state=WineAdderState.sugar)
async def add_wine_set_sugar(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['sugar'] = int(call.data.split(':')[1])
        print(data['sugar'])
    
    await call.message.answer("По цвету:", reply_markup=create_four_button(color_dict))
    await WineAdderState.next()
    

# add color
# req country 
@dp.callback_query_handler(state=WineAdderState.color)
async def add_wine_set_color(call: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['color'] = int(call.data.split(':')[1])
        print(data['color'])
    
    await call.message.answer("Теперь напиши страну производителя?") 
    await WineAdderState.next()


# add country
# req producer 
@dp.message_handler(state=WineAdderState.country)
async def add_wine_set_country(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['country'] = message.text
        print(data['country'])
    
    
    await message.answer("Кто производитель (компания/винодельня)?") 
    await WineAdderState.next()


# add producer
# req year 
@dp.message_handler(state=WineAdderState.producer)
async def add_wine_set_producer(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['producer'] = message.text
        print(data['producer'])
    
    await message.answer("Какой год урожая?") 
    await WineAdderState.next()


# add year
# req location 
@dp.message_handler(state=WineAdderState.year)
async def add_wine_set_year(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['year'] = int(message.text)
        print(data['year'])
    
    await message.answer("Где происходило сие распитие? (если помнишь)") 
    await WineAdderState.next()


# add location
# req price 
@dp.message_handler(state=WineAdderState.location)
async def add_wine_set_location(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.text
        print(data['location'])
    
    await message.answer("Сколько стоило це превосходство?") 
    await WineAdderState.next()


# add price
# req comment 
@dp.message_handler(state=WineAdderState.price)
async def add_wine_set_price(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
        print(data['price'])
    
    await message.answer("comment ????") 
    await WineAdderState.next()


# add price
# req comment 
@dp.message_handler(state=WineAdderState.comment)
async def add_wine_set_comment(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text
        print(data['comment'])
    
    # todo add to db
    # await add_to_database(state=state,data=data)

    print(data)
    # add wine into db 

# sent to log chat
    end = time.time() - start ## собственно время работы программы
    await message.bot.send_message(channel_log_id, f"""
#wine - new wine
username: {message.from_user.username}\n
complete {end:.3f}""")

    await commands.add_wine(
        created_by = message.from_user.id,
        image = data['photo'],
        wine = data['wine'].lower().strip(),
        score = data['score'],
        grape = data['grape'].lower().strip(),
        sugar = data['sugar'],
        color = data['color'],
        country = data['country'],
        producer = data['producer'],
        year = data['year'],
        location = data['location'],
        price = data['price'],
        comment = data['comment']
        )

    await message.answer("готово") 
    await state.finish()





# 
#    ___       SEARCH WINE     ___
# 



# requesting search options
@dp.message_handler(text = '/search')
async def search_wine(message: types.Message, state: FSMContext):
    await WineSearchState.search.set()
    await message.answer("Как будем искать твое вено??", reply_markup=create_four_button(search_options, search_query))

    # sent to log chat
    await message.bot.send_message(channel_log_id, f"""
#wine - new search request
username: {message.from_user.username}\n""")


# 1 option - name
@dp.callback_query_handler(search_query.filter(num = '1'), state=WineSearchState.search)
async def search_wine_by_name(call: types.CallbackQuery, state: FSMContext):

    await call.message.answer("Как зовут твое вено??")
    await WineSearchState.serch_by_name.set()


# requesting search options - name
@dp.message_handler(state=WineSearchState.serch_by_name)
async def search_wine_by_name_searching(message: types.Message, state: FSMContext):
    
    request = message.text.lower().strip()
    result = await commands.select_wine_by_name(wine_name=request, user_id=message.from_user.id)

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
@dp.callback_query_handler(search_query.filter(num = '2'), state=WineSearchState.search)
async def search_wine_by_sugar(call: types.CallbackQuery, state: FSMContext):

    await call.message.answer("Выбирай", reply_markup=create_four_button(sugar_dict))
    await WineSearchState.serch_by_sugar.set()


# requesting search options - sugar
@dp.callback_query_handler(state=WineSearchState.serch_by_sugar)
async def search_wine_by_sugar_searching(call: types.CallbackQuery, state: FSMContext):
    

    request = int(call.data.split(':')[1])
    result = await commands.select_wine_by_sugar(wine_sugar=request, user_id=call.message.chat.id)

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
@dp.callback_query_handler(search_query.filter(num = '3'), state=WineSearchState.search)
async def search_wine_by_color(call: types.CallbackQuery, state: FSMContext):

    await call.message.answer("Выбирай", reply_markup=create_four_button(color_dict))
    await WineSearchState.serch_by_color.set()

# requesting search options - color
@dp.callback_query_handler(state=WineSearchState.serch_by_color)
async def search_wine_by_color_searching(call: types.CallbackQuery, state: FSMContext):
    
    print(call.data)
    request = int(call.data.split(':')[1])
    result = await commands.select_wine_by_color(wine_color=request, user_id=call.message.chat.id)

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
@dp.callback_query_handler(search_query.filter(num = '4'), state=WineSearchState.search)
async def search_wine_by_name(call: types.Message, state: FSMContext):

    await call.message.answer("Как зовут твое вено??")
    await WineSearchState.serch_by_name.set()
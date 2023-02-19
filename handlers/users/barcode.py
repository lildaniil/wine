from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, channel_log_id

from utils.db_api import commands
from utils.stat.set_stats import set_stat_data
from utils.misc import barcode_reader

from states import AddBarcode


@dp.message_handler(text='/bar')
@dp.message_handler(text='/barcode')
async def bot_start(message: types.Message):
    await AddBarcode.bc_photo.set()
    await message.answer("Загрузи фото штрихкода")


@dp.message_handler(content_types=['photo'], state=AddBarcode.bc_photo)
async def add_wine_set_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bc_photo'] = message.photo[-1].file_id

        path = barcode_reader.set_path()

        await message.photo[-1].download(path)

        
        get_code = barcode_reader.get_code(path)

        if get_code != None:
            type, barcode_numbers = get_code

            data['bc_type'] = type
            data['bc_numbers'] = barcode_numbers

            await message.answer("Теперь сфотографируй этикетку на бутылке, чтобы можно было понять, что это за вино")
            await AddBarcode.next()

        else: 
            await message.answer("Штрих-код не найден, попробуй еще раз!\nИли жми /отмена")
            await AddBarcode.bc_photo.set()



@dp.message_handler(content_types=['photo'], state=AddBarcode.wine_photo)
async def add_wine_set_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['wine_photo'] = message.photo[-1].file_id


        await commands.add_barcode(
            created_by=message.from_user.id,
            bc_image=data['bc_photo'],
            bc_number=data['bc_numbers'],
            type=data['bc_type'],
            wine_image=data['wine_photo']
        )

        await message.bot.send_message(channel_log_id, f"""
#wine - barcode was added
username: {message.from_user.username}""")

        await message.answer("ФЕНКЬЮ ФЕНКЬЮ, ДАРЛИНГ")

        await state.finish()
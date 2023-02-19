from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(state='*', text='Отмена')
@dp.message_handler(state='*', text='отмена')
@dp.message_handler(state='*', text='/отмена')
@dp.message_handler(state='*', text='/отмена')
@dp.message_handler(state='*', text='/cancel')
async def bot_cancel(message: types.Message, state: FSMContext):

    await state.finish() 
    await message.answer("Отмена")

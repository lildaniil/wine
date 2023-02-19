from aiogram import types
import random

def random_name(symbols=8, pas:str='processed_'):
    
    for x in range(symbols):
        pas = pas + random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
    return pas


class TempPicture():

    async def __init__(self, path):
        self.path = path
        self.name = random_name(pas='add_')

    async def get_name(self):
        return self.name

    
    async def save(self, message : types.Message):
        await message.photo[-1].download(self.path+'/'+str(self.name)+".jpg")
        pass


    def delete():
        pass


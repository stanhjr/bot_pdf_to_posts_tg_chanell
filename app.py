import os
import time
import sqlite3
from aiogram.dispatcher import Dispatcher
from aiogram.types import InputMediaPhoto
from aiogram.utils import executor
from aiogram import Bot, types
from pdf2image import convert_from_path
from config import TOKEN
from config import CHANNEL

connection = sqlite3.connect(r'test.db')
cursor = connection.cursor()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message):
    fence = '=' * 32
    cursor.execute("SELECT * FROM pd_test;")
    one_result = cursor.fetchall()
    for row in one_result:
        time.sleep(60)
        project = f'Номер проекта {row[1]}'
        order = f'Номер заказа {row[2]}'
        image_path = row[3]
        message_pp = f'{fence}\n {project}\n{fence}\n{order}\n{fence}'
        await bot.send_message(CHANNEL, message_pp)
        pages = convert_from_path(image_path, 150)
        media = []
        
        # page pdf to jpg
        for i, page in enumerate(pages):
            print(len(pages))
            path_jpg = f'{order}{i}.jpg'
            page.save(path_jpg, 'JPEG')
            img = open(path_jpg, 'rb')
            if len(pages) == 1:
                await bot.send_photo(CHANNEL, img)
                break
            elif i <= 10:
                print(path_jpg)
                media.append(InputMediaPhoto(img))
            else:
                await bot.send_photo(CHANNEL, img)
        if len(pages) > 1:
            await bot.send_media_group(CHANNEL, media=media)
        # delete temp files
        for i, page in enumerate(pages):
            path_jpg = f'{order}{i}.jpg'
            os.remove(path_jpg)

    connection.commit()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

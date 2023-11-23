import logging
import os
from enum import Enum
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

import db
import qr

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users = {}


class Modes(Enum):
    TITLE = 1
    DESCRIPTION = 2


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id = message.chat.id
    users[user_id] = {}
    users[user_id]['mode'] = Modes.TITLE
    await message.answer("Привет! Введи название объекта, который хочешь добавить: ")


@dp.message_handler()
async def echo(message: types.Message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        users[user_id]['mode'] = Modes.TITLE
    if users[user_id]['mode'] == Modes.TITLE:
        users[user_id]['title'] = message.text
        users[user_id]['mode'] = Modes.DESCRIPTION
        await message.reply('Теперь отправь описание:')
    elif users[user_id]['mode'] == Modes.DESCRIPTION:
        users[user_id]['desc'] = message.text
        users[user_id]['mode'] = Modes.TITLE
        qr_id = db.insert(users[user_id]['title'], users[user_id]['desc'], user_id)
        await bot.send_photo(user_id, qr.get_qr_code(str(qr_id)))
        await message.reply('Теперь название:')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
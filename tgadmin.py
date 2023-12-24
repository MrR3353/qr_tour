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
    NOTHING = 3
    DELETE = 4
    GET_QR = 5


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        users[user_id]['mode'] = Modes.NOTHING
    users[user_id] = {}
    users[user_id]['mode'] = Modes.NOTHING
    await message.answer("Привет! Используй команды через /!")


@dp.message_handler(commands=['delete'])
async def delete_qr(message: types.Message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        users[user_id]['mode'] = Modes.NOTHING
    users[user_id]['mode'] = Modes.DELETE
    await message.answer("Введите ID QR-кода для удаления:")

@dp.message_handler(commands=['create'])
async def create_qr(message: types.Message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        users[user_id]['mode'] = Modes.NOTHING
    users[user_id]['mode'] = Modes.TITLE
    await message.answer("Введите название объекта:")

@dp.message_handler(commands=['getQR'])
async def get_qr(message: types.Message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        users[user_id]['mode'] = Modes.NOTHING
    users[user_id]['mode'] = Modes.GET_QR
    await message.answer("Введите ID объекта:")

@dp.message_handler(commands=['getAll'])
async def get_all_records(message: types.Message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        users[user_id]['mode'] = Modes.NOTHING
    records = db.get_all_by_user_id(user_id)

    if not records:
        await message.answer("У вас нет сохраненных записей.")
    else:
        response_text = "Ваши записи:\n"
        for record in records:
            response_text += f"ID: {record['id']}, Заголовок: {record['title']}, Описание: {record['desc']}\n\n\n"
        await message.answer(response_text)

@dp.message_handler()
async def echo(message: types.Message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {}
        users[user_id]['mode'] = Modes.NOTHING
    if users[user_id]['mode'] == Modes.TITLE:
        users[user_id]['title'] = message.text
        users[user_id]['mode'] = Modes.DESCRIPTION
        await message.reply('Теперь отправь описание:')
    elif users[user_id]['mode'] == Modes.DESCRIPTION:
        users[user_id]['desc'] = message.text
        users[user_id]['mode'] = Modes.NOTHING
        qr_id = db.insert(users[user_id]['title'], users[user_id]['desc'], user_id)
        await bot.send_photo(user_id, qr.get_qr_code(str(qr_id)))
    elif users[user_id]['mode'] == Modes.DELETE:
        try:
            qr_id = message.text
            db.delete_qr_by_id(qr_id, user_id)
            await message.answer(f"QR-код с ID {qr_id} успешно удален.")
        except ValueError:
            await message.answer("Неверный формат ID. Введите корректное число.")
        finally:
            users[user_id]['mode'] = Modes.NOTHING
    elif users[user_id]['mode'] == Modes.GET_QR:
        await bot.send_photo(user_id, qr.get_qr_code(message.text))
        users[user_id]['mode'] = Modes.NOTHING

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

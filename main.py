import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import asyncio
import os

# Завантажуємо токен з .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Перевірка, чи токен зчитано
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено у файлі .env. Переконайтесь, що файл .env містить BOT_TOKEN=ваш_токен")

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Створюємо клавіатуру
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="НАШ ВЕБСАЙТ"), KeyboardButton(text="СТОРІНКА ФБ")],
        [KeyboardButton(text="Онлайн запис")]
    ],
    resize_keyboard=True
)

# Обробник команди /start з клавіатурою
@dp.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.reply("Оберіть опцію:", reply_markup=keyboard)

# Обробник натискань кнопок
@dp.message(lambda message: message.text in ["НАШ ВЕБСАЙТ", "СТОРІНКА ФБ", "Онлайн запис"])
async def handle_buttons(message: types.Message):
    if message.text == "НАШ ВЕБСАЙТ":
        await message.reply("Відвідай наш вебсайт: <a href='https://297975.wixsite.com/gaicnap'>НАШ ВЕБСАЙТ</a>")
    elif message.text == "СТОРІНКА ФБ":
        await message.reply("Перейди на нашу сторінку у Facebook: <a href='https://www.facebook.com/gai.chnap'>СТОРІНКА ФБ</a>")
    elif message.text == "Онлайн запис":
        await message.reply("Перейди за посиланням для онлайн запису: <a href='https://cherga.diia.gov.ua/app/thematic_area_office/350'>Онлайн запис</a>")

# Запуск бота
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не знайдено.")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("НАШ ВЕБСАЙТ", url="https://haisynska-gromada.gov.ua"))
    keyboard.add(InlineKeyboardButton("СТОРІНКА ФБ", url="https://www.facebook.com/haisynska.gromada"))
    keyboard.add(InlineKeyboardButton("Онлайн запис", url="https://haisynska-gromada.gov.ua/booking"))
    await message.answer("Вітаємо в офіційному боті ЦНАП Гайсинської громади! 👋 Оберіть опцію:", reply_markup=keyboard)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
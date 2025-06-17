from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
logging.info(f'BOT_TOKEN: {BOT_TOKEN}')
if not BOT_TOKEN:
    raise ValueError('BOT_TOKEN не знайдено.')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: types.Message):
    logging.info(f'Received /start from {message.from_user.id}')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='НАШ ВЕБСАЙТ', url='https://297975.wixsite.com/gaicnap')],
        [InlineKeyboardButton(text='СТОРІНКА ФБ', url='https://www.facebook.com/gai.chnap')],
        [InlineKeyboardButton(text='Онлайн запис', url='https://cherga.diia.gov.ua/app/thematic_area_office/350')]
    ])
    await message.answer('Вітаємо в офіційному боті ЦНАП Гайсинської громади! 👋 Оберіть опцію:', reply_markup=keyboard)

if __name__ == '__main__':
    import asyncio
    async def main():
        logging.info('Starting polling...')
        await dp.start_polling(bot, skip_updates=True)
    asyncio.run(main())

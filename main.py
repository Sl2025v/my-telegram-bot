import os
import feedparser
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot = Bot(token="8154400685:AAHndHpdhTIi8hEs-Nk-UVxr0Xom5BRAwZQ")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("НАШ ВЕБСАЙТ", url="https://297975.wixsite.com/gaicnap"))
    keyboard.add(types.InlineKeyboardButton("СТОРІНКА ФБ", url="https://www.facebook.com/gai.chnap"))
    keyboard.add(types.InlineKeyboardButton("Онлайн запис", url="https://cherga.diia.gov.ua/app/thematic_area_office/350"))
    await message.reply("Вітаю! Оберіть опцію:", reply_markup=keyboard)

@dp.message_handler(commands=['news'])
async def send_news(message: types.Message):
    feed = feedparser.parse("http://fetchrss.com/rss/68554af6b931f9efab0720a368554b11611fe25418090fc2.xml")
    await message.reply(f"Debug: Status={feed.status}, Entries={len(feed.entries)}")
    if feed.entries:
        news = "\n\n".join(f"{entry.title}: {entry.summary if 'summary' in entry else entry.link}" for entry in feed.entries[:5])
        await message.reply(f"Останні новини:\n{news[:4096]}")
    else:
        await message.reply("Немає доступних новин.")

if __name__ == '__main__':
    if os.environ.get('RUN_MAIN') == 'true':
        executor.start_polling(dp, skip_updates=True)
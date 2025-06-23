import os
import feedparser
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import fcntl
import time

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
        news_items = []
        for entry in feed.entries[:5]:
            item = f"{entry.title}: {entry.summary if 'summary' in entry else entry.link}"
            news_items.append(item)
        news_text = "\n\n".join(news_items)
        chunk_size = 4096
        for i in range(0, len(news_text), chunk_size):
            await message.reply(news_text[i:i + chunk_size] or "Немає додаткового тексту.")
    else:
        await message.reply("Немає доступних новин.")

def run_bot():
    if os.environ.get('RUN_MAIN') == 'true':
        lock_file = '/tmp/bot.lock'
        fp = open(lock_file, 'w')
        try:
            fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
            executor.start_polling(dp, skip_updates=True)
        except IOError:
            print("Another instance is running, exiting...")
            return
        finally:
            fp.close()

if __name__ == '__main__':
    run_bot()
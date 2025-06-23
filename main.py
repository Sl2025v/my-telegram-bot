import os
import feedparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook

# Ініціалізація бота з пам’яттю
bot = Bot(token="8154400685:AAHndHpdhTIi8hEs-Nk-UVxr0Xom5BRAwZQ")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Обробники команд
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

# Налаштування Webhook
WEBHOOK_HOST = 'https://gai-cnap-bot.onrender.com'  # Заміни на твій URL
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Функція запуску
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print("Webhook встановлено!")

async def on_shutdown(dp):
    await bot.delete_webhook()
    print("Webhook видалено!")

if __name__ == '__main__':
    if os.environ.get('RUN_MAIN') == 'true':
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host='0.0.0.0',
            port=8080
        )
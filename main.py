import os
import feedparser
import signal
import sys
import pip
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiohttp import web

print(f"Pip version: {pip.__version__}")

bot_token = os.environ.get('BOT_TOKEN', '8154400685:AAHndHpdhTIi8hEs-Nk-UVxr0Xom5BRAwZQ')
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="НАШ ВЕБСАЙТ", url="https://297975.wixsite.com/gaicnap")],
        [types.InlineKeyboardButton(text="СТОРІНКА ФБ", url="https://www.facebook.com/gai.chnap")],
        [types.InlineKeyboardButton(text="Онлайн запис", url="https://cherga.diia.gov.ua/app/thematic_area_office/350")]
    ])
    await message.reply("Вітаю! Оберіть опцію:", reply_markup=keyboard)

@dp.message(Command("news"))
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

WEBHOOK_HOST = 'https://gai-cnap-bot-web.onrender.com'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print("Webhook встановлено!")

async def on_shutdown(dp):
    await bot.delete_webhook()
    print("Webhook видалено!")

def signal_handler(sig, frame):
    print('Received SIGTERM, shutting down...')
    sys.exit(0)

async def handle_webhook(request):
    update = await request.json()
    Dispatcher.update_outer_queue.put_nowait(update)
    return web.Response(text="OK")

async def main():
    port = int(os.environ.get('PORT', 10000))
    print(f"Binding to port {port} on 0.0.0.0")
    signal.signal(signal.SIGTERM, signal_handler)
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host='0.0.0.0', port=port)
    await site.start()
    print("Web server started")

    # Замість start_polling запускаємо цикл обробки подій
    await dp.start_polling(bot)  # Додаємо bot як аргумент, якщо потрібно, але краще уникати для вебхука
    # Для вебхука достатньо запуску сервера, опитування не потрібне
    # Замість цього просто тримаємо цикл
    await asyncio.Event().wait()  # Тримаємо процес активним

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
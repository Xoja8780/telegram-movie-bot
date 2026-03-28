import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers import start, films, watchlist, trailer
import logging
from database.database import init_db
from dotenv import load_dotenv
import os


# 🚀 Инициализация бота и диспетчера

async def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Роутеры
    dp.include_router(start.router)
    dp.include_router(films.router)
    dp.include_router(watchlist.router)
    dp.include_router(trailer.router)

    logging.basicConfig(level=logging.INFO)
    print("Бот запущен 🚀")

    # Инициализация базы данных
    await data_startup()

    # Запуск бота
    await dp.start_polling(bot)


async def data_startup():
    await init_db()
    print("База данных готова 🚀")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен ❌")

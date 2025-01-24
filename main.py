import asyncio

from aiogram import Dispatcher, Bot
from dishka import make_async_container
from dishka.integrations.aiogram import setup_dishka


from application.handlers import router
from config import Config
from ioc import AppProvider


async def start_bot():
    config = Config()
    bot_container = make_async_container(AppProvider(), context={Config: config})

    dp = await bot_container.get(Dispatcher)
    bot = await bot_container.get(Bot)

    setup_dishka(router=dp, container=bot_container, auto_inject=True)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())

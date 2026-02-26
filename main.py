import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config.config import BOT_TOKEN
from handlers import router as main_router
from services.set_bot_commands import set_default_commands
from services.notify_admins import on_startup_notify
from services.db_api.sql_lite import Database


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(main_router)

    db = Database()
    await db.create_tables()

    await set_default_commands(bot)
    await on_startup_notify(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

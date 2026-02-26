from aiogram import Bot
from config.config import ADMINS


async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "Bot ishga tushdi 🚀")
        except:
            pass

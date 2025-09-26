import os
import asyncio

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.strategy import FSMStrategy

from handlers.user_private import user_private_router
from common.bot_cmds import private

ALLOWED_UPDATES = ["message"]
load_dotenv()
bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(fsm_strategy= FSMStrategy.USER_IN_CHAT)
dp.include_routers(user_private_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES, polling_timeout=2)

asyncio.run(main())
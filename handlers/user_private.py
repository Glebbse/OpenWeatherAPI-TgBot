from aiogram import Router, types
from aiogram.filters import Command

from common.bot_cmds import text_commands
# from open_weather_tg_bot.filters.chat_types import ChatTypeFilter

from aiogram.filters import CommandStart


user_private_router = Router()
# user_private_router.message.filter(ChatTypeFilter(["private"]))

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("This is Hello-message, I'm OpenWeatherBot. Click on the menu to see available commands :)")

@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("This bot uses open-source API of OpenWeather company to get Current and forecasts weather data in your city.\n\n"
                         "Read more: https://openweather.co.uk/about.\n\n"
                         "Official Website: https://openweathermap.org.")

@user_private_router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    text = f"Available commands:\n" + "\n".join(text_commands)
    await message.answer(text)

@user_private_router.message(Command("current_weather"))
async def current_weather_cmd(message: types.Message):
    await message.answer("Enter your city:\nExample: London")

@user_private_router.message(Command("daily_forecast"))
async def daily_forecast_cmd(message: types.Message):
    await message.answer("This command in development")

@user_private_router.message(Command("hourly_forecast"))
async def hourly_forecast_cmd(message: types.Message):
    await message.answer("This command in development")

@user_private_router.message(Command("minutely_forecast"))
async def minutely_forecast_cmd(message: types.Message):
    await message.answer("This command in development")
from time import sleep

from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter
from kbds import reply
from weather_funcs import get_weather


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

class AddCity(StatesGroup):
    gettingCity = State()
    gettingForecast = State()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("<b><i>This is Hello-message, I'm OpenWeatherBot. Click something in menu. </i></b> 😊",
                         reply_markup=reply.get_kbd(
                             "about",
                             "Enter city",
                              placeholder="What's your interest?",
                             sizes=(1,1)
                         )
)

@user_private_router.message(StateFilter(None), Command("enter_city"))
@user_private_router.message((F.text.lower() == "enter city") | (F.text.lower() == "enter place") | (F.text.lower().contains("city")))
async def enter_city_cmd(message: types.Message, state: FSMContext):
    await message.answer("<b><i>Enter your city:\nExample: London</i></b>", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddCity.gettingCity)

@user_private_router.message(StateFilter("*"),F.text.casefold().contains("cancel"))
@user_private_router.message(StateFilter("*"),Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("<i><b>Actions were cancelled</b></i>",
                         reply_markup=reply.get_kbd(
                             "about",
                             "Enter city",
                             placeholder="Type smth 😊",
                             sizes=(1,1)
                         )
    )

@user_private_router.message(StateFilter(None), F.text.lower() == "about")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("This bot uses open-source API of OpenWeather company to get Current and forecasts weather data in your city.\n\n"
                         "Read more: https://openweather.co.uk/about.\n\n"
                         "Official Website: https://openweathermap.org.", reply_markup=reply.get_kbd(
        "about",
        "Enter city",
        placeholder="What's your interest?",
        sizes=(1,1)
    ))

@user_private_router.message(AddCity.gettingCity, F.text)
async def adding_city(message: types.Message, state: FSMContext):
    city_name = message.text.capitalize()
    user_data = await state.update_data(city=city_name)
    print(user_data)
    geo_result = get_weather.get_geo(city=user_data.get("city"))
    if isinstance(geo_result, str):
        await message.answer(f"<b><i>'{geo_result}'</i></b>")
        await message.answer("<b><i>Enter your city:\nExample: London</i></b>", reply_markup=types.ReplyKeyboardRemove())
        return
    await message.answer(
    "<i><b>City's added\n\nWhat forecast do you want to get?</b></i>",
        reply_markup=reply.get_kbd(
            "Current weather",
            "Daily forecast",
            "Hourly forecast",
            "Minutely forecast",
            "cancel",
            placeholder="What forecast are you interested in?",
            sizes=(2,2)
        )
    )
    await state.set_state(AddCity.gettingForecast)
    lati, long = geo_result
    await state.update_data(lati=lati, long=long)


@user_private_router.message(StateFilter(None), F.text.lower() == "about")
@user_private_router.message(Command("about"))
async def about_cmd(message: types.Message):
    await message.answer("This bot uses open-source API of OpenWeather company to get Current and forecasts weather data in your city.\n\n"
                         "Read more: https://openweather.co.uk/about.\n\n"
                         "Official Website: https://openweathermap.org.", reply_markup=reply.get_kbd(
        "about",
        "Enter city",
        placeholder="What's your interest?",
        sizes=(1,1)
    ))

@user_private_router.message(AddCity.gettingForecast, F.text.lower() == "current weather", F.text.lower().contains("current"))
@user_private_router.message(Command("current_weather"))
async def current_weather_cmd(message: types.Message, state: FSMContext):
    await message.answer("<i><b>Getting forecast...</b></i>")
    await state.update_data(forecast=message.text)
    user_data = await state.get_data()

    weather = get_weather.get_weather(lat=user_data.get("lati"), lon=user_data.get("long"))
    await message.answer(f"<i><b>{get_weather.format_current_weather(city=user_data.get("city"), data=weather)}</b></i>")
    await state.set_state(AddCity.gettingCity)
    await message.answer("<i><b>What are you going to see next?</b></i>", reply_markup=reply.get_kbd(
        "enter new city/place",
        "Current weather",
        "Daily forecast",
        "Hourly forecast",
        "Minutely forecast",
        "Cancel",
        placeholder="What is your interest?",
        sizes=(2,2,1)
    ))

@user_private_router.message(F.text.lower() == "daily forecast")
@user_private_router.message(Command("daily_forecast"))
async def daily_forecast_cmd(message: types.Message, state: FSMContext):
    await message.answer("This command in development")

@user_private_router.message(F.text.lower() == "hourly forecast")
@user_private_router.message(Command("hourly_forecast"))
async def hourly_forecast_cmd(message: types.Message, state: FSMContext):
    await message.answer("This command in development")

@user_private_router.message(F.text.lower() == "minutely forecast")
@user_private_router.message(Command("minutely_forecast"))
async def minutely_forecast_cmd(message: types.Message, state: FSMContext):
    await message.answer("This command in development")





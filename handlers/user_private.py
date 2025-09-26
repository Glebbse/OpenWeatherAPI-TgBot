from collections.abc import Callable

from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter
from kbds import reply
from weather_funcs import get_weather


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

class GetForecast(StatesGroup):
    gettingCity = State()
    gettingForecastMenu = State()
    gettingForecast = State()
    DailyForecastReply = State()
    HourlyForecastReply = State()

@user_private_router.message(StateFilter("*"), F.text.lower().contains("menu"))
async def forecast_menu(message: types.Message, state: FSMContext):
    await state.set_state(GetForecast.gettingForecast)
    await forecast_weather_options(message, state)

async def forecast_weather_options(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f"<i><b>forecast menu. City: {user_data.get("city")}\nWhat forecast are you interested in?</b></i>", reply_markup=reply.get_kbd(
        "enter new city/place",
        "Current weather",
        "Daily forecast",
        "Hourly forecast",
        "Cancel",
        placeholder="What is your interest?",
        sizes=(2,2,1)
    ))


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

@user_private_router.message(StateFilter(None),  Command("enter_city"))
@user_private_router.message((F.text.lower() == "enter city") | (F.text.lower() == "enter place") | (F.text.lower().contains("city")))
async def opening(message: types.Message, state: FSMContext):
    await message.answer("<b><i>Enter your city:\nExample: London</i></b>", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(GetForecast.gettingCity)

@user_private_router.message(StateFilter("*"), F.text.casefold().contains("cancel"))
@user_private_router.message(StateFilter("*"), Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("<i><b>Actions have been cancelled</b></i>",
                         reply_markup=reply.get_kbd(
                             "about",
                             "Enter city",
                             placeholder="Type smth 😊",
                             sizes=(1,1)
                         )
    )

@user_private_router.message(GetForecast.gettingCity, F.text)
async def adding_city(message: types.Message, state: FSMContext):
    city_name = message.text.capitalize()
    await state.update_data(city=city_name)
    geo_result = get_weather.get_geo(city=city_name)
    if isinstance(geo_result, str):
        await message.answer(f"<b><i>'{geo_result}'</i></b>")
        await message.answer("<b><i>Enter your city:\nExample: London</i></b>", reply_markup=types.ReplyKeyboardRemove())
        return
    lati, long = geo_result
    await state.update_data(lati=lati, long=long)
    await forecast_weather_options(message, state)
    await state.set_state(GetForecast.gettingForecast)

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

@user_private_router.message(GetForecast.gettingForecast, (F.text.lower() == "current weather") | (F.text.lower().contains("current")))
@user_private_router.message(Command("current_weather"))
async def current_weather(message: types.Message, state: FSMContext):
    exclude = "daily,hourly,minutely"
    await message.answer("<i><b>Getting current weather...</b></i>")
    user_data = await state.update_data(forecast_current=message.text)
    coordinates = get_weather.get_weather(lat=user_data.get("lati"), lon=user_data.get("long"), exclude=exclude)
    await message.answer(f"<i><b>{get_weather.format_current_weather(city=user_data.get("city"), data=coordinates)}</b></i>")
    await current_weather_options(message, state)

async def current_weather_options(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(f"<i><b>City: {user_data.get("city")}\nWhat are you going to see next?</b></i>", reply_markup=reply.get_kbd(
        "enter new city/place",
        "Current weather",
        "Daily forecast",
        "Hourly forecast",
        "Forecast menu"
        "Cancel",
        placeholder="What is your interest?",
        sizes=(2,2,2)
    ))


@user_private_router.message(GetForecast.gettingForecast, (F.text.lower() == "daily forecast") | (F.text.lower().contains("daily")))
@user_private_router.message(Command("daily_forecast"))
async def daily_forecast(message: types.Message, state: FSMContext):
    exclude = "current,hourly,minutely"
    user_data = await state.update_data(forecast_daily=message.text)
    daily_weather = get_weather.get_weather(lat=user_data.get("lati"), lon=user_data.get("long"), exclude=exclude)
    await message.answer("<i><b>Getting daily forecast...</b></i>")
    await state.update_data(daily_weather=daily_weather)
    await daily_forecast_options(message, state)
    await state.set_state(GetForecast.DailyForecastReply)

async def daily_forecast_options(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer("<i><b>8 days forecast has been got.</b></i>")
    await message.answer(f"<i><b>City: {user_data.get("city")}\nWhat day are you interested in?</b></i>",
                         reply_markup=reply.get_kbd(
                             "Day 1",
                             "Day 2",
                             "Day 3",
                             "Day 4",
                             "Day 5",
                             "Day 6",
                             "Day 7",
                             "Day 8",
                             "Forecast menu",
                             "cancel",
                             placeholder="Your choice",
                             sizes=(3,3,3,1)
                         ))

@user_private_router.message(GetForecast.DailyForecastReply, F.text.lower().contains("day"))
async def daily_forecast_reply(message: types.Message, state: FSMContext):
    chosen_day = int(message.text.split()[1]) - 1
    user_data = await state.update_data(chosen_day=chosen_day)
    daily_forecast_data = get_weather.format_daily_forecast(city=user_data.get("city"), data=user_data.get("daily_weather"), day=user_data.get("chosen_day"))
    await message.answer(f"<b><i>{daily_forecast_data}</i></b>")
    await daily_forecast_options(message, state)

@user_private_router.message(StateFilter(GetForecast.gettingForecast), F.text.lower() == "hourly forecast")
@user_private_router.message(Command("hourly_forecast"))
async def hourly_forecast(message: types.Message, state: FSMContext):
    exclude = "current,daily,minutely"
    await message.answer("<i><b>Getting hourly forecast...</b></i>")
    user_data = await state.update_data(forecast_hourly=message.text)
    hourly_weather = get_weather.get_weather(lat=user_data.get("lati"), lon=user_data.get("long"), exclude=exclude)
    await hourly_forecast_options(message, state)
    await state.update_data(hourly_weather=hourly_weather)
    await state.set_state(GetForecast.HourlyForecastReply)
    print(hourly_weather)

async def hourly_forecast_options(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer("<i><b>24 hours forecast has been got.</b></i>")
    await message.answer(f"<i><b>City: {user_data.get("city")}\n What hour are you interested in?</b></i>", reply_markup=reply.get_kbd(
        "Hours 1-3",
        "Hours 4-6",
        "Hours 7-9",
        "Hours 10-12",
        "Hours 13-15",
        "Hours 16-18",
        "Hours 19-21",
        "Hours 22-24",
        "Go to forecast menu",
        "cancel",
        placeholder="Your choice?",
        sizes=(3,3,4)
    ))


@user_private_router.message(StateFilter(GetForecast.HourlyForecastReply, F.text.lower().contains("hours")))
async def hourly_forecast_reply(message: types.Message, state: FSMContext):
    chosen_hours = message.text
    user_data = await state.update_data(chosen_hours=chosen_hours)
    hourly_weather_data = get_weather.format_hourly_forecast(city=user_data.get("city"), data=user_data.get("hourly_weather"), customer_input=user_data.get("chosen_hours"))
    await message.answer(f"<i><b>{hourly_weather_data}</b></i>")
    await hourly_forecast_options(message, state)


@user_private_router.message(GetForecast.gettingForecast, F.text.lower().contains("city"))
async def edit_city(message: types.Message, state: FSMContext):
    await message.answer(f"<i><b>Change your city.</b></i>", reply_markup=types.ReplyKeyboardRemove())
    new_city = message.text
    await message.answer("<i><b>City's changed.</b></i>")
    user_data = await state.update_data(city=new_city)

# @user_private_router.message(StateFilter('*'), F.text)
# async def invalid_input(message: types.Message):
#     await message.reply("Invalid input")


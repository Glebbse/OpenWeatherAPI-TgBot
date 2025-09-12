from aiogram.types import BotCommand

private = [
    BotCommand(command="about", description="About this bot"),
    BotCommand(command="menu", description="Get the menu of commands"),
    BotCommand(command="current_weather", description="Get current weather"),
    BotCommand(command="daily_forecast", description="Get daily forecast for 8 days"),
    BotCommand(command="hourly_forecast", description="Get hourly forecast for 48 hours"),
    BotCommand(command="minutely_forecast", description="Get forecast for next 60 minutes")
]

text_commands = ["/about", "/current_weather", "/daily_forecast", "/hourly_forecast", "/minutely_forecast"]
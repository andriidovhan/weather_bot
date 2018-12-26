#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler
from weather import Weather, Unit
import telegram
import os


WEATHER = Weather(unit=Unit.CELSIUS)


def get_weather(city):
    location = WEATHER.lookup_by_location(city)
    condition = location.condition
    return ("""Today is: {},
    "Current temp: {},
    "Summary: {}""".format(condition.date, condition.temp, condition.text))


def get_forecast(city):
    location = WEATHER.lookup_by_location(city)
    forecasts_list = []
    forecasts = location.forecast
    for forecast in forecasts[:3]:
        forecasts_list.append("""{}
                Max/Min: {}/{}
                Summary: {}""".format(forecast.date, forecast.high, forecast.low, forecast.text))
    return "\n".join(forecasts_list)


def start(bot, update):
    update.message.reply_text("I'm a weather bot.")


def weather(bot, update, args=[]):
    # set default value
    city = args[0] if bool(args) else 'kharkiv'
    update.message.reply_text(get_weather(city))


def forecast(bot, update, args=[]):
    city = args[0] if bool(args) else 'kharkiv'
    bot.send_message(chat_id=update.message.chat_id, text=get_forecast(city),
                     parse_mode=telegram.ParseMode.HTML)


def help(bot, update):
    # custom_commands = ["/start", "/get_weather", "/forecast", "/help"]
    custom_commands = """/start\n/weather\n/forecast\n/help"""
    update.message.reply_text(custom_commands)


def main():
    # Create Updater object and attach dispatcher to it
    updater = Updater(config.TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('help', help))
    print("Bot started")

    # Add command handler to dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    weather_handler = CommandHandler('weather', weather, pass_args=True)
    dispatcher.add_handler(weather_handler)

    forecast_handler = CommandHandler('forecast', forecast, pass_args=True)
    dispatcher.add_handler(forecast_handler)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()

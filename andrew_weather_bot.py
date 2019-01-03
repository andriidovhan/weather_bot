#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, InlineQueryHandler
from model.weatherEntitiy import WeatherEntity
import telegram
import os
import logging
import currency_rate
import hryvna_today

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text("I'm a weather bot.")


def weather(bot, update, args=[]):
    # set default value
    city = args[0] if bool(args) else 'kharkiv'
    weather_instanse = WeatherEntity(city)
    logger.info(" Get weather for '{}' city.".format(city))
    update.message.reply_text("=== {} ==\n {}".format(city, weather_instanse.get_current_weather()))
    bot.send_photo(chat_id=update.message.chat_id,
                   photo=weather_instanse.get_weather_image())


def forecast(bot, update, args=[]):
    city = args[0] if bool(args) else 'kharkiv'
    logger.info(" Get forecast for '{}' city.".format(city))
    weather_instanse = WeatherEntity(city)
    bot.send_message(chat_id=update.message.chat_id,
                     text="=== {} ==\n {}".format(city, weather_instanse.get_forecast()),
                     parse_mode=telegram.ParseMode.HTML)


def help(bot, update):
    custom_commands = """/start\n/weather\n/forecast\n/rate\n/hryvna\n/help"""
    update.message.reply_text(custom_commands)


def rate(bot, update, args=[]):
    update.message.reply_text(currency_rate.get_rate(args))


def hryvna(bot, update, args=[]):
    update.message.reply_text(hryvna_today.get_rate(args))


def unknown(bot, update):
    logger.warning(
        "Unknown command is entered: '{}' by '{}'.".format(update.message['text'], update.message['chat']['username']))
    update.message.reply_text("Sorry, I don't know that command.")


def inlinequery(bot, update):
    weather_instanse = WeatherEntity('kharkiv')
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="share_weather",
            input_message_content=InputTextMessageContent(
                weather_instanse.get_current_weather())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="share_forecast",
            input_message_content=InputTextMessageContent(
                weather_instanse.get_forecast()))]

    update.inline_query.answer(results)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create Updater object and attach dispatcher to it
    updater = Updater(os.environ.get('TOKEN'))
    dispatcher = updater.dispatcher

    print("Bot started")

    # Add command handler to dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('weather', weather, pass_args=True))
    dispatcher.add_handler(CommandHandler('forecast', forecast, pass_args=True))
    dispatcher.add_handler(CommandHandler('rate', rate, pass_args=True))
    dispatcher.add_handler(CommandHandler('hryvna', hryvna, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()

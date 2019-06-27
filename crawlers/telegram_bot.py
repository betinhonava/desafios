import logging
import os

from scrapper import RedditScrapper
from telegram.ext import CommandHandler, Updater

logging.basicConfig(filename='bot.log', level=logging.ERROR)


def nada_pra_fazer(bot, context, args=[]):
    scrapper = RedditScrapper(*args)
    for thread in scrapper.run(format='list'):
        context.message.reply_text(thread)


updater = Updater(os.environ.get('TELEGRAM_API_TOKEN', None))

updater.dispatcher.add_handler(
    CommandHandler('NadaPraFazer', nada_pra_fazer, pass_args=True))
updater.start_polling()
updater.idle()

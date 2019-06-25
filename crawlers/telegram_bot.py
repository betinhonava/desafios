from telegram.ext import Updater, CommandHandler
import os


def nada_pra_fazer(bot, context, args=[]):
    pass


updater = Updater(os.environ.get('TELEGRAM_API_TOKEN', None))

updater.dispatcher.add_handler(CommandHandler('NadaPraFazer', nada_pra_fazer, pass_args=True))
updater.start_polling()
updater.idle()
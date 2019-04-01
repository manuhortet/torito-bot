import logging
import os

import bot.memify as memify
import telegram
from bot.credentials import token
from bot.new_meme import TORERO, TORITO, cancel, new, torero, torito
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot = telegram.Bot(token=token)


def start(bot, update):
    output = os.path.dirname(os.path.abspath(__file__)) + "/torito.gif"

    memify.memify_torito(torito_text="this bot", torero_text="your shitty memes", output=output)
    bot.sendDocument(chat_id=update.message.chat_id, document=open(output, 'rb'))

    logging.info('Bot running for: @{} ({})'.format(update.effective_user.username, update.effective_user.full_name))


def unknown(bot, update):
    output = os.path.dirname(os.path.abspath(__file__)) + "/torito.gif"

    memify.memify_torito(torito_text="Telegram bots API", torero_text="manuhortet", output=output)
    bot.sendDocument(chat_id=update.message.chat_id, document=open(output, 'rb'))


def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="")


def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('new', new)],
        states={
            TORITO: [MessageHandler(Filters.text, torito)],
            TORERO: [MessageHandler(Filters.text, torero)]},
        fallbacks=[CommandHandler('cancel', cancel)]))
    dispatcher.add_handler(MessageHandler(Filters.text, unknown))

    updater.start_polling()
    updater.idle()

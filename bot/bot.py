import logging
import os
import sys

import bot.memify as memify
import telegram
from bot.credentials import token
from bot.new_meme import TORERO, TORITO, cancel, new, torero, torito
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

token = "694638932:AAE6vOQ1_Wuo2dM5X0hGSaBiPqwm3V6KfSE"

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = telegram.Bot(token=token)


def start(bot, update):
    path = os.path.dirname(os.path.abspath(__file__))
    output = path + "/torito.gif"
    memify.memify_torito(torito_text="este bot", torero_text="tus memes de mierda", output=output)
    bot.sendDocument(chat_id=update.message.chat_id, document=open(output, 'rb'))
    logging.info("Bot started. Action by: ", update.effective_user.first_name)
    if update.effective_user.first_name == "Dani":
            bot.sendMessage(chat_id=update.message.chat_id, text="Your credentials coincide! I have a secret message for you:\n\nManu loves you <3")


def unknown(bot, update):
    path = os.path.dirname(os.path.abspath(__file__))
    output = path + "/torito.gif"
    memify.memify_torito(torito_text="Telegram bots API", torero_text="manuhortet", output=output)
    bot.sendDocument(chat_id=update.message.chat_id, document=open(output, 'rb'))
    logging.info("Unkown message received. Message:", update.message.text,
                 "Action by: ", update.effective_user.first_name)


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

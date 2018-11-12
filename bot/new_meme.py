import logging
import os
import sys

import bot.memify as memify

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

TORITO, TORERO = range(2)

# Conversational states for the /new CommandHandler

text = []


def new(bot, update):
    global text
    text = []
    bot.sendMessage(chat_id=update.message.chat_id, text="(Cancel the process at any point using /cancel)\n\nText for the bull:")
    return TORITO


def torito(bot, update):
    text.append(update.message.text)
    bot.sendMessage(chat_id=update.message.chat_id, text="Text for the bullfighter:")
    return TORERO


def torero(bot, update):
    text.append(update.message.text)

    # memify
    path = os.path.dirname(os.path.abspath(__file__))
    output = path + "/torito.gif"
    memify.memify_torito(torito_text=text[0], torero_text=text[1], output=output)
    bot.sendDocument(chat_id=update.message.chat_id, document=open(output, 'rb'))
    logging.info("New meme - TEXT: \"{}\", \"{}\" - ACTION BY: @{}"
                 .format(text[0], text[1], update.effective_user.username))

    return -1


def cancel(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Canceled!")
    logging.info("Canceled meme - ACTION BY: @{}".format(update.effective_user.username))
    return -1

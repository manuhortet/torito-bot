import os

import bot.memify as memify

TORITO, TORERO = range(2)

# Conversational states for the /new CommandHandler

text = []


def new(bot, update):
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

    return -1


def cancel(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Canceled!")
    return -1

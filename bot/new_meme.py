import logging
import os
import bot.memify as memify

TORITO, TORERO = range(2)
text = []


def new(bot, update):
    global text
    text = []
    bot.sendMessage(chat_id=update.message.chat_id, text="(Cancel the process at any point using /cancel)\n\n\U0001F42E Text for the bull:")
    return TORITO


def torito(bot, update):
    text.append(update.message.text)
    bot.sendMessage(chat_id=update.message.chat_id, text="\U0001F915 Text for the bullfighter:")
    return TORERO


def torero(bot, update):
    text.append(update.message.text)

    path = os.path.dirname(os.path.abspath(__file__))
    output = path + "/torito.gif"
    memify.memify_torito(torito_text=text[0], torero_text=text[1], output=output)
    bot.sendDocument(chat_id=update.message.chat_id, document=open(output, 'rb'))

    logging.info("New meme: \"{}\", \"{}\" for: @{} ({})"
                 .format(text[0], text[1],
                         update.effective_user.username,
                         update.effective_user.full_name))
    return -1


def cancel(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Canceled!")

    logging.info("Canceled meme by: @{}"
                 .format(update.effective_user.username,
                         update.effective_user.full_name))
    return -1

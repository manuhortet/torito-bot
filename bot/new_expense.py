import datetime
from bot.credentials.credentials import google_credentials

NAME, CATEGORY, PRICE, DATE, DATE_2, PLACE, ONLINE, FOR_WHO, EXTRA = range(9)
new_expense = []

def format(user_input):
    return user_input[0].upper() + user_input[1:].lower()

# Conversational states for the /new command

def new(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="(Cancel the process at any point using /cancel)\n\nName the expense:")
    new_expense = []
    return NAME

def name(bot, update):
    new_expense.append(format(update.message.text))
    bot.sendMessage(chat_id=update.message.chat_id, text="Category:")
    return CATEGORY

def category(bot, update):
    new_expense.append(format(update.message.text))
    bot.sendMessage(chat_id=update.message.chat_id, text="Price:")
    return PRICE

def price(bot, update):
    new_expense.append(format(update.message.text))
    bot.sendMessage(chat_id=update.message.chat_id, text="Have you just made the expense?: (y/n)")
    return DATE

def date(bot, update):
    if update.message.text[0].lower() == 'y':
        now = datetime.datetime.now()
        formated_date = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
        new_expense.append(formated_date)
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="OK, introduce the date then: ")
        return DATE_2
    bot.sendMessage(chat_id=update.message.chat_id, text="Place:")
    return PLACE

def date_2(bot, update):
    new_expense.append(update.message.text)
    return PLACE

def place(bot, update):
    new_expense.append(format(update.message.text))
    bot.sendMessage(chat_id=update.message.chat_id, text="The expense was made online?: (y/n)")
    return ONLINE

def online(bot, update):
    new_expense.append(1) if update.message.text[0].lower() == "y" else new_expense.append(0)
    bot.sendMessage(chat_id=update.message.chat_id, text="Who made the expense?: (c/d/m)")
    return FOR_WHO

def for_who(bot, update):
    mapper = {"c": (1, 0, 0), "d": (0, 1, 0), "m": (0, 0, 1)}
    new_expense.extend(mapper[update.message.text.lower()])
    bot.sendMessage(chat_id=update.message.chat_id, text="Any comment to add?:")
    return EXTRA

def extra(bot, update):
    if update.message.text.lower() != "no":
        new_expense.append(format(update.message.text))
    google_credentials.open('Expenses').get_worksheet(1).append_row(new_expense, value_input_option="USER_ENTERED")
    new_expense.clear()
    bot.sendMessage(chat_id=update.message.chat_id, text="The new expense was tracked succesfully.")
    return -1

def cancel(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Canceled!")
    return -1

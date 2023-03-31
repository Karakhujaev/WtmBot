import pandas 
from get_data import *
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from telegram.ext.filters import Filters


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hi {update.effective_user.first_name}')
    update.message.reply_text(f'You can search music')

def search(update: Update, context: CallbackContext) -> None:
    searched = update.message.text

    # result = session.query(Table).filter(Table.name==searched)
    result = session.query(Table).filter_by(name=searched).first()
    import pandas 
from get_data import *
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from telegram.ext.filters import Filters


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hi {update.effective_user.first_name}')
    update.message.reply_text(f'You can search music')

def search(update: Update, context: CallbackContext) -> None:
        searched = update.message.text

        # result = session.query(Table).filter_by(name=searched).first()
        # print(result)
        result = session.query(Table).filter_by(author=searched).all()
        print(result)
        for i in range(len(result)):
            mus = result[i]
            caption = f'{mus.name}\n{mus.author}'
            update.message.reply_text(f'{mus.link} \n {caption}')

    # caption = f'{result.name}\n{result.author}'
    # update.message.reply_text(f'{result.link} \n {caption}')
    # update.message.reply_text(f'{result.link}')
    

updater = Updater('5141714174:AAGoxJEX4-2ndRln3W00c5SJqhXeftxXD58')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, search))

updater.start_polling()
updater.idle()
    # update.message.reply_text(f'{result.link}')
    

updater = Updater('5141714174:AAGoxJEX4-2ndRln3W00c5SJqhXeftxXD58')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, search))

updater.start_polling()
updater.idle()
from ast import Try
from telegram import Update, message
from email.mime import audio
from get_data import*
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, CallbackQueryHandler
from telegram.ext.filters import Filters
import requests
from bs4 import BeautifulSoup
import os

info = []
buttons = []
like_dislike = []
song_number = 0
favourites = []
history = []
times = 1
ad_urls = ''


def start(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hi {update.effective_user.first_name}')
    update.message.reply_text(f'You can search music')

def search(update: Update, context: CallbackContext):
    global info, times, history, buttons, like_dislike, favourites
    times = 1
    message = ""
    like = 0
    dislike = 0
    history.append([info])
    info.clear()

    chat_id = update.effective_chat.id
    
    buttons = [
        [
            InlineKeyboardButton('1', callback_data='btn0'),
            InlineKeyboardButton('2', callback_data='btn1'),
            InlineKeyboardButton('3', callback_data='btn2'),
            InlineKeyboardButton('4', callback_data='btn3'),
            InlineKeyboardButton('5', callback_data='btn4')
        ],
        [
            InlineKeyboardButton('6', callback_data='btn5'),
            InlineKeyboardButton('7', callback_data='btn6'),
            InlineKeyboardButton('8', callback_data='btn7'),
            InlineKeyboardButton('9', callback_data='btn8'),
            InlineKeyboardButton('10', callback_data='btn9')
        ],
        [ 
            InlineKeyboardButton('⏮', callback_data='btn10'),
            InlineKeyboardButton('❌', callback_data='btn11'),
            InlineKeyboardButton('⏭', callback_data='btn12')
        ]
    ]

  
    
    searched = update.message.text
    lowered = searched.lower()
    capitalized = searched.title()
    uppered = searched.upper()

    titles = [searched, lowered, capitalized, uppered]

    for method in titles:
        if session.query(Table).filter_by(author=method).all(): 
        
                result = session.query(Table).filter_by(author=method).all()

                for x in range(len(result)):
                    link = result[x].link
                    music_name = result[x].name
                    music_auth = result[x].author
                    info.append([music_auth, music_name, link, like])

        if session.query(Table).filter_by(name=method).all(): 
        
                result = session.query(Table).filter_by(name=method).all()

                for x in range(len(result)):
                    link = result[x].link
                    music_name = result[x].name
                    music_auth = result[x].author
                    
                    info.append([music_auth, music_name, link, like])
    for i in range(len(info)):
        if i < 10:
            singer = info[i][0]
            music = info[i][1]
            link = info[i][2]
            index = i+1
            message += f"{index}. {singer} - {music}\n\n"

    context.bot.send_message(chat_id=chat_id,text=message, reply_markup=InlineKeyboardMarkup(buttons))
   

def button(update: Update, context: CallbackContext):
    global info, times, buttons, ad_urls, like_dislike, favourites, song_number

    chat_id = update.effective_chat.id
    query = update.callback_query

    like_dislike = [
        [
            InlineKeyboardButton('❤️', callback_data='btn13'),
            InlineKeyboardButton(f'👍', callback_data='btn14')
        ]
    ]

    if query.data == f'btn11':
        query.message.delete()

    elif query.data == f'btn12':
        message = ''
        fir = int(f"{times}0")
        sec = int(f"{times+1}0")
        index=0
        ad_urls = []
        for i in range(fir, sec):
            if i < sec:
                song_number = i
                singer = info[i][0]
                music = info[i][1]
                ad_urls.append([info[i][0], info[i][1], info[i][2]])
                index+=1
                message += f"{index}. {singer} - {music}\n\n"
        context.bot.send_message(chat_id=chat_id,text=message, reply_markup=InlineKeyboardMarkup(buttons))
        query.message.delete()
        times+=1

    elif query.data == f'btn10' and times > 1:
        message = ''
        times -= 1
        fir = int(f"{times-1}0")
        sec = int(f"{times}0")
        index=0
        ad_urls = []
        for i in range(fir, sec):
            if i < sec:
                song_number = i
                singer = info[i][0]
                music = info[i][1]
                ad_urls.append([info[i][0], info[i][1], info[i][2]])
                index+=1
                message += f"{index}. {singer} - {music}\n\n"
        context.bot.send_message(chat_id=chat_id,text=message, reply_markup=InlineKeyboardMarkup(buttons))
        query.message.delete()

    elif times > 1:
        for x in range(10):  
            if query.data == f'btn{x}':
                author = ad_urls[x][0]
                name = ad_urls[x][1]
                song_number = x
                url = ad_urls[x][2]
                song = requests.get(url)
                with open(f'my_song.mp3', 'wb') as f:
                    f.write(song.content)
                caption = f'{author} - {name}\n\nhttps://t.me/muz_zonebot'
                context.bot.send_audio(chat_id, open('my_song.mp3','rb'),  reply_markup=InlineKeyboardMarkup(like_dislike), caption=caption)

    elif  times == 1:                
        for x in range(10):  
            if query.data == f'btn{x}':
                author = info[x][0]
                name = info[x][1]
                url = info[x][2]
                song_number = x
                song = requests.get(url)
                with open(f'my_song.mp3', 'wb') as f:
                    f.write(song.content)
                caption = f'{author} - {name}\n\nhttps://t.me/muz_zonebot'
                context.bot.send_audio(chat_id, open('my_song.mp3','rb'),  reply_markup=InlineKeyboardMarkup(like_dislike), caption=caption)

    if query.data == f'btn14':
        info[song_number][3] += 1
        print(info[song_number][3])

    elif query.data == f'btn13':
        favourites.append(info[song_number])
        print(favourites)

def list(update: Update, context: CallbackContext):
    global favourites, song_number
    chat_id = update.effective_chat.id
    
    message = ''

    for i in range(len(favourites)):
        if i < 10:
            singer = favourites[i][0]
            music = favourites[i][1]
            link = favourites[i][2]
            index = i+1
            message += f"{index}. {singer} - {music}\n\n"

    context.bot.send_message(chat_id=chat_id,text=message, reply_markup=InlineKeyboardMarkup(buttons))

    
updater = Updater('5340525544:AAF8vQO2n6IS6sXeKwHjcjuVSf3p-77RRdY')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('list', list))
updater.dispatcher.add_handler(MessageHandler(Filters.text, search))
updater.dispatcher.add_handler(CallbackQueryHandler(button))



updater.start_polling()
print('Active')
updater.idle()
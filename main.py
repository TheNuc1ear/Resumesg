from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence, CallbackContext, CallbackQueryHandler, ConversationHandler, CallbackContext
from telegram.utils import helpers
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
from dotenv import load_dotenv
import psycopg2
import random
from DBManagement import NEWENTRY, GETREFERRER, UPDATE_NOOFREF, GETNOOFREF

load_dotenv()
# Postgresql stuff

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = con.cursor()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = str(user.id)
    username = user.username
    user_firstname = user.first_name
    REFCODE = user_id
    referrerid = update.message.text.strip('/start ')
    print(referrerid)

    cur.execute('SELECT USERID FROM TGMUSERS WHERE USERID = %s', (user_id,))
    checkUserid = cur.fetchall()
    if len(checkUserid) == 0:
        print("New User")
        NEWENTRY(user_id, username, user_firstname, REFCODE, referrerid, 0)
        greeting = "Hello {}! Welcome to ResumeSG Bot".format(user_firstname)
        update.message.reply_text(greeting)
        REFERRER_username = GETREFERRER(referrerid)
        REFERRER_username = str(REFERRER_username[0])
        print(REFERRER_username[0])
        chatmessage = "Your referrer is:- {}".format(REFERRER_username)
        referror_message = "{} signed up using your link!".format(
            user_firstname)
        context.bot.send_message(
            chat_id=referrerid,
            text=referror_message
        )
        UPDATE_NOOFREF(referrerid)
        update.message.reply_text(chatmessage)
    else:
        print("Old User")
        greeting = "Welcome back {}. \nUse /referral for more info on your referrals".format(
            user_firstname)
        update.message.reply_text(greeting)


def referral(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = str(user.id)
    Noofref = GETNOOFREF(user_id)
    Noofref = int(Noofref[0])
    bot = context.bot
    reflink = helpers.create_deep_linked_url(bot.username, user_id)
    linkbeg = "https://t.me/share/url?url="
    newreflink = linkbeg + reflink
    msg = "You have referred a total of {} people".format(Noofref)
    update.message.reply_text(msg)
    reply_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Forward", url=newreflink)],
    ])
    update.message.reply_text(
        f'Click button to choose chats to forward it to',
        reply_markup=reply_buttons
    )

































def botmain():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    print("starting bot")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('referral', referral))


    updater.start_polling()
    updater.idle()

botmain()

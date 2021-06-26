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
        greeting = "Hello {}! Welcome to ResumeSG Bot.\nUse /referral for more info on your referrals.\nUse /form to fill up our form and place an order".format(user_firstname)
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
        greeting = "Welcome back {}.\nUse /referral for more info on your referrals.\nUse /form to fill up our form and place an order ".format(
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
    newreflink = linkbeg + reflink + "\nUse this link to sign up and get your own digital profile!"
    msg = "You have referred a total of {} people.\n You'll prob get cashback or some shit if you refer 5 people and they buy our service. \n_bopz_ ".format(Noofref)
    update.message.reply_text(msg, parse_mode="Markdown")
    user_sticker = 'CAACAgQAAxkBAAECfB1g12GgGJKASDuZ-MizpHlaben5BgACvgsAArxBaFEPMnV3RgEmxSAE'
    context.bot.sendSticker(
        chat_id=update.effective_chat.id,
        sticker=user_sticker
    )
    reply_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Forward", url=newreflink)],
    ])
    update.message.reply_text(
        f'Choose chats to forward your referral link to',
        reply_markup=reply_buttons
    )

def form(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = str(user.id)
    username = user.username
    formurl = "https://docs.google.com/forms/d/e/1FAIpQLSdvzQQFwjq3c90K0F1kRik3lPn6GERhMF7km_zRl3ANW_pvbQ/viewform?usp=pp_url&entry.223422261=" + str(username)
    reply_buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Fill me up NOW", url=formurl)],
    ])
    update.message.reply_text(
        "Fill up the form to place an order".format(username),
        reply_markup=reply_buttons,
        parse_mode="html"
    )
































def botmain():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    print("starting bot")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('referral', referral))
    dp.add_handler(CommandHandler('form', form))


    updater.start_polling()
    updater.idle()

botmain()

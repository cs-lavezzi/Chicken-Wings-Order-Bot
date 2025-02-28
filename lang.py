from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

from main import *


def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Uzbek', 'English', 'Russian']]
    update.message.reply_text(
        'Welcome! Please choose your language:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return LANG


def choose_lang(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s has chosen their language: %s", user.first_name, update.message.text)
    update.message.reply_text('Please enter your name:')
    return NAME

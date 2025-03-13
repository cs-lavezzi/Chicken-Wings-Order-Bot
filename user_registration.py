import logging
from telegram import Update
from telegram.ext import ContextTypes
from main import VERIFY, CONTACT, ORDER, LOCATION


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logging.info(f"User {user.first_name} has entered their name: {update.message.text}")
    await update.message.reply_text('Please enter your contact number:')
    return CONTACT

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logging.info(f"User {user.first_name} has entered their contact number: {update.message.text}")
    await update.message.reply_text('A verification code has been sent to your contact number. Please enter the code:')
    return VERIFY

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    if update.message.location:
        location_data = f"Latitude: {update.message.location.latitude}, Longitude: {update.message.location.longitude}"
        logging.info(f"User {user.first_name} has shared their location: {location_data}")
    else:
        logging.warning(f"User {user.first_name} did not share their location properly.")
    await update.message.reply_text('We will send you an SMS for verification.')
    logging.info(f"Sending SMS verification code to user {user.first_name}")
    return VERIFY

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text('Verification successful! You can now place your order.')
    return ORDER
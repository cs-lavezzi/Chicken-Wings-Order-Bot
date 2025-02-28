from telegram import Update
from telegram.ext import CallbackContext
import logging

from main import *


def name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logging.info(f"User {user.first_name} has entered their name: {update.message.text}")
    update.message.reply_text('Please enter your contact number:')
    return CONTACT


def contact(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logging.info(f"User {user.first_name} has entered their contact number: {update.message.text}")
    update.message.reply_text('A verification code has been sent to your contact number. Please enter the code:')
    return VERIFY


def location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    if update.message.location:
        location_data = f"Latitude: {update.message.location.latitude}, Longitude: {update.message.location.longitude}"
        logging.info(f"User {user.first_name} has shared their location: {location_data}")
    else:
        logging.warning(f"User {user.first_name} did not share their location properly.")
    update.message.reply_text('We will send you an SMS for verification.')
    # Logging to simulate sending SMS verification.
    logging.info(f"Sending SMS verification code to user {user.first_name}")
    return VERIFY


def verify(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text('Verification successful! You can now place your order.')
    # Here you would verify the code
    return ORDER
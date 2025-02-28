from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

def order(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text('Please choose from the menu:')
    # Here you would present the interactive menu
    return ConversationHandler.END
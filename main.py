import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from registration import name, contact, location, verify
from order import order
from lang import start, choose_lang

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states
LANG, NAME, CONTACT, LOCATION, VERIFY, ORDER = range(6)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels the conversation and ends it."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation. Message text: '%s'", user.first_name, update.message.text)
    await update.message.reply_text('Bye! Hope to see you again soon.')
    return ConversationHandler.END

def main() -> None:
    """Runs the bot using webhook."""
    bot_token = "7937053541:AAFBhf4CPwNiaCV1KmU59Fy0aSPxDSUNW4w"  # Replace with your bot token
    webhook_url = "https://yourdomain.com/your_webhook_path"  # Replace with your webhook URL

    try:
        application = Application.builder().token(bot_token).build()
        logger.info("Bot application initialized successfully with the provided token.")
    except Exception as e:
        logger.error("Error initializing bot application: %s", str(e))
        return

    # Configure the ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_lang)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, contact)],
            LOCATION: [MessageHandler(filters.LOCATION, location)],
            VERIFY: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify)],
            ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, order)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    try:
        application.add_handler(conv_handler)
        logger.info("ConversationHandler added successfully.")
    except Exception as e:
        logger.error("Error adding ConversationHandler: %s", str(e))
        return

    # Webhook setup
    try:
        application.run_webhook(
            listen="0.0.0.0",  # Address to listen on
            port=8443,  # Port exposed for webhook traffic
            url_path="your_webhook_path",  # URL path for the webhook
            webhook_url=webhook_url  # Your webhook URL
        )
        logger.info("Webhook started successfully on 0.0.0.0:8443 with path 'your_webhook_path'")
    except Exception as e:
        logger.error("Error starting webhook: %s", str(e))

if __name__ == '__main__':
    main()
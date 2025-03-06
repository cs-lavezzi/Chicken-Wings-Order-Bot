import logging
import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiohttp import web
from aiogram.types import Update
from main import bot

load_dotenv()

# Logging settings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)

# Telegram bot secret token for validation
TELEGRAM_SECRET_TOKEN = os.getenv("BOT_TOKEN") # add your token here from .env file
if not TELEGRAM_SECRET_TOKEN:
    raise ValueError("TELEGRAM_SECRET_TOKEN must be set in environment variables!")

# Webhook settings
WEBHOOK_HOST = os.getenv("WEBHOOK_URL") # https://your.domain
if not WEBHOOK_HOST:
    raise ValueError("WEBHOOK_HOST must be set in environment variables!")

WEBHOOK_PATH = "/webhook" # Should match the path that was set on webhook creation
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}" # Full path to webhook

# Server settings
WEBAPP_HOST = "0.0.0.0"  # Local server
WEBAPP_PORT = 8080 # Port for the server

dp = Dispatcher()

async def handle_webhook(request):
    """ Accepts incoming webhook requests """
    logging.info("Webhook request received")

    # Check the Telegram secret token
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != TELEGRAM_SECRET_TOKEN:
        logging.warning("Unauthorized access detected.")
        return web.Response(status=403, text="Forbidden")

    update = Update(**await request.json()) # Correctly parse the update
    await dp.process_update(update) # Dispatch the update to the dp
    return web.Response(text="OK")


async def on_startup():
    """ When bot is started webhook URL is set """
    try:
        await bot.set_webhook(WEBHOOK_URL, secret_token=TELEGRAM_SECRET_TOKEN)
        logging.info(f"Webhook set up at {WEBHOOK_URL}")
    except Exception as e:
        logging.error(f"Failed to set webhook: {e}")


async def on_shutdown():
    """ When bot is stopped webhook URL is deleted """
    await bot.session.close()


# AIOHTTP server initialization
app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle_webhook)
app.on_startup.append(on_startup) # Pass the coroutine function directly
app.on_shutdown.append(on_shutdown) # Pass the coroutine function directly

# Start the server
if __name__ == "__main__":
    web.run_app(app, host=WEBAPP_HOST,
                port=WEBAPP_PORT)
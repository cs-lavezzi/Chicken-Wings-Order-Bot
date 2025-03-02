import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web
from dotenv import load_dotenv

load_dotenv() # .env faylini yuklash

# Bot tokeni va webhook URL
TOKEN = ("7937053541:AAFBhf4CPwNiaCV1KmU59Fy0aSPxDSUNW4w")
WEBHOOK_HOST = ("https://76cb-37-110-215-71.ngrok-free.app") # https://your.domain
WEBHOOK_PATH = "/webhook" # Webhook URL
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Server sozlamalari
WEBAPP_HOST = "0.0.0.0"  # Lokal server
WEBAPP_PORT = 8080

# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratish
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage()) # MemoryStorage bilan Dispatcher yaratish

# Foydalanuvchi tilini saqlash uchun dict
user_language = {}

# /start kommandasi uchun handler
@dp.message()
async def start_cmd(message: types.Message):
    if message.text == "/start":
        await message.answer("Tilni tanlang:", reply_markup=language_keyboard())

# Til tanlash tugmalari
def language_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz"),
         InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
         InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ])
    return keyboard

# Tilni tanlash callback funksiyasi
@dp.callback_query(lambda c: c.data.startswith("lang_"))
async def change_language(callback: CallbackQuery, state: FSMContext):
    lang_code = callback.data.split("_")[1]
    user_id = callback.from_user.id

    # Foydalanuvchining tanlagan tilini saqlaymiz
    user_language[user_id] = lang_code

    # Til o'zgargani haqida habar yuboramiz
    messages = {
        "uz": "Til O'zbek tiliga o'zgartirildi ✅",
        "ru": "Язык изменён на Русский ✅",
        "en": "Language changed to English ✅"
    }

    await callback.message.answer(messages[lang_code])
    await callback.answer()

@dp.message()
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    lang = user_language.get(user_id, "uz")  # Agar til tanlanmagan bo'lsa, "uz"

    messages = {
        "uz": "Assalomu alaykum! Botga xush kelibsiz.",
        "ru": "Здравствуйте! Добро пожаловать в бот.",
        "en": "Hello! Welcome to the bot."
    }

    await message.answer(messages[lang], reply_markup=language_keyboard())

# Webhookni sozlash
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook o'rnatildi: {WEBHOOK_URL}")

async def on_shutdown():
    await bot.delete_webhook()
    logging.info("Webhook o'chirildi.")

# Webhookni qabul qilish uchun handler
async def handle_webhook(request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return web.Response(text="OK")

# Web serverni ishga tushirish
async def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    # Botni ishga tushirish
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEBAPP_HOST, WEBAPP_PORT)
    await site.start()

    await on_startup()
    try:
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        await on_shutdown()

if __name__ == "__main__":
    asyncio.run(main())

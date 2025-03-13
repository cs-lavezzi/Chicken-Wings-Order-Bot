import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from firebase_google_sheets_integration import save_user_language, get_user_language

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Language selection
language_button = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="🇺🇿 O'zbekcha"),
            KeyboardButton(text="🇷🇺 Русский"),
            KeyboardButton(text="🇬🇧 English")
        ]
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start_command(message: types.Message):
    """ When user is starting the bot then this function will be called """
    user_id = message.from_user.id
    lang = get_user_language(user_id) # Getting user language from Firebase
    await message.answer("Tilni tanlang! ✅", reply_markup=language_button)


@dp.message()
async def select_language(message: types.Message):
    """ User selects the language and saves it to Firebase """
    user_id = message.from_user.id
    text = message.text.lower()

    languages = {"🇺🇿 o'zbekcha": "uz", "🇷🇺 русский": "ru", "🇬🇧 english": "en"}

    if text in languages:
        save_user_language(user_id, languages[text]) # Saving user language to Firebase
        await message.answer("Til tanlandi! ✅")
    else:
        await message.answer("Tilni tanlang! ✅", reply_markup=language_button)

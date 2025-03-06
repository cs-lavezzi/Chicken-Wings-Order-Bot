# lang.py

LANGUAGES = ["uz", "ru", "en"]  # Supported languages

MESSAGES = {
    "start": {
        "uz": "Til tanlandi! ✅ Endi buyurtma berishingiz mumkin.",
        "ru": "Язык выбран! ✅ Теперь вы можете оформить заказ.",
        "en": "Language selected! ✅ Now you can place an order."
    },
    "order": {
        "uz": "Buyurtma berish uchun mahsulotni tanlang 🍔",
        "ru": "Выберите продукт, чтобы заказать 🍔",
        "en": "Choose a product to order 🍔"
    },
    "payment": {
        "uz": "To‘lov usulini tanlang: Click, Payme yoki naqd 💳",
        "ru": "Выберите способ оплаты: Click, Payme или наличные 💳",
        "en": "Choose a payment method: Click, Payme, or cash 💳"
    }
}

def get_message(key, lang):
    """Returns the message in the user's language."""
    return MESSAGES.get(key, {}).get(lang, MESSAGES.get(key, {}).get("uz", "Message not found"))

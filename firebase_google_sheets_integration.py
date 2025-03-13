import firebase_admin
from firebase_admin import credentials, firestore
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Firebase xizmat hisobini yuklash
cred = credentials.Certificate("JSON/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
      "databaseURL": "https://fir-order-bot-default-rtdb.europe-west1.firebasedatabase.app"
})

# Firestore bilan bog'lash
db = firestore.client()

# Foydalanuvchi tilini saqlash
def save_user_language(user_id: int, language: str):
    """Foydalanuvchi tilini Firebase-da saqlash."""
    db.collection("users").document(str(user_id)).set({"language": language}, merge=True)

# Foydalanuvchi tilini olish
def get_user_language(user_id: int) -> str:
    """Foydalanuvchi tilini Firebase-dan olish. Agar yo‘q bo‘lsa, 'uz' qaytariladi."""
    doc = db.collection("users").document(str(user_id)).get()
    if doc.exists:
        return doc.to_dict().get("language", "uz")
    return "uz"

# Foydalanuvchi ma'lumotlarini saqlash
def save_user_data(user_id: int, user_data: dict):
    """Foydalanuvchi haqida qo‘shimcha ma'lumotlarni saqlash."""
    db.collection("users").document(str(user_id)).set(user_data, merge=True)

# Foydalanuvchi ma'lumotlarini olish
def get_user_data(user_id: int) -> dict:
    """Foydalanuvchi haqida barcha ma'lumotlarni olish."""
    doc = db.collection("users").document(str(user_id)).get()
    if doc.exists:
        return doc.to_dict()
    return {}

# Buyurtmalarni Firebase-ga saqlash
def save_order(user_id: int, order_data: dict):
    """Foydalanuvchi buyurtmasini Firebase-da saqlash."""
    order_ref = db.collection("orders").document()
    order_data["user_id"] = user_id
    order_data["order_id"] = order_ref.id  # Unikal order ID
    order_ref.set(order_data)

# Foydalanuvchi buyurtmalarini olish
def get_orders(user_id: int):
    """Foydalanuvchining barcha buyurtmalarini olish."""
    orders = db.collection("orders").where("user_id", "==", user_id).stream()
    return [order.to_dict() for order in orders]
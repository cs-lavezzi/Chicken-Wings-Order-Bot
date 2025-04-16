chicken-wings-order-bot/
│
├── bot/                # Bot asosiy modullari
│   ├── __init__.py
│   ├── main.py         # Asosiy bot skripti
│   ├── config.py       # Konfiguratsiya sozlamalari
│   ├── handlers/       # Bot buyruqlarini boshqaruvchi modullar
│   │   ├── __init__.py
│   │   ├── start.py    # /start va boshlang'ich menyu
│   │   ├── language.py # Til boshqaruvi
│   │   ├── menu.py     # Menyu bilan ishlash
│   │   ├── cart.py     # Savat boshqaruvi
│   │   ├── order.py    # Buyurtma berish
│   │   └── payment.py  # To'lov usullari
│   │
│   ├── services/       # Qo'shimcha xizmatlar
│   │   ├── __init__.py
│   │   ├── firebase.py # Firebase bilan ishlash
│   │   ├── sheets.py   # Google Sheets bilan ishlash
│   │   ├── sms.py      # SMS tasdiqlash
│   │   └── payment.py  # Click va Payme integratsiyasi
│   │
│   └── utils/          # Yordam funksiyalar
│       ├── __init__.py
│       ├── keyboards.py# Tugmalar va menyu
│       └── validators.py # Ma'lumotlarni tekshirish
│
├── admin/              # Admin panel
│   ├── __init__.py
│   ├── app.py          # Flask admin paneli
│   ├── routes.py       # Admin panel marshrutlari
│   └── forms.py        # Admin uchun formalar
│
├── config/             # Konfiguratsiya fayllar
│   ├── __init__.py
│   ├── development.py  # Rivojlanish rejimi sozlamalari
│   └── production.py   # Ishga tushirish rejimi sozlamalari
│
├── requirements.txt    # Kerakli kutubxonalar ro'yxati
├── .env                # Maxfiy o'zgaruvchilar
├── .gitignore          # Git-ga qo'shmaslik kerak bo'lgan fayllar
└── README.md           # Loyiha haqida asosiy ma'lumot
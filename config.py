import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

ADMIN_IDS = [
    int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
]

CARD_NUMBER = os.getenv("CARD_NUMBER", "0000 0000 0000 0000")
CARD_HOLDER = os.getenv("CARD_HOLDER", "F.I.Sh.")

# Railway / Docker uchun /data papkasi tavsiya etiladi (persistent volume)
# Lokal ishlatganda oddiy "bot.db" ham ishlaydi
DB_PATH = os.getenv("DB_PATH", "bot.db")

# --- Mahsulotlar katalogi ---
# Stars paketlari: (nomi, miqdori, narxi so'mda)
STARS_PACKAGES = [
    {"id": "stars_15", "title": "15 ⭐", "amount": 15, "price_sum": 5000},
    {"id": "stars_25", "title": "25 ⭐", "amount": 25, "price_sum": 8000},
    {"id": "stars_50", "title": "50 ⭐", "amount": 50, "price_sum": 15000},
    {"id": "stars_100", "title": "100 ⭐", "amount": 100, "price_sum": 28000},
    {"id": "stars_250", "title": "250 ⭐", "amount": 250, "price_sum": 68000},
    {"id": "stars_500", "title": "500 ⭐", "amount": 500, "price_sum": 129400},
    {"id": "stars_1000", "title": "1000 ⭐", "amount": 1000, "price_sum": 255500},
]

# Premium paketlari: (nomi, muddati, narxi so'mda)
PREMIUM_PACKAGES = [
    {"id": "premium_1", "title": "Premium — 1 oy", "months": 1, "price_sum": 95000},
    {"id": "premium_3", "title": "Premium — 3 oy", "months": 3, "price_sum": 187600},
    {"id": "premium_6", "title": "Premium — 6 oy", "months": 6, "price_sum": 221800},
    {"id": "premium_12", "title": "Premium — 12 oy", "months": 12, "price_sum": 415500},
]

# 1 Stars narxi (agar Telegram Stars orqali to'lansa, taxminiy kurs)
# Buni real vaziyatga qarab sozlang
SUM_PER_STAR_PRICE = 1  # narxlar allaqachon paketlarda ko'rsatilgan

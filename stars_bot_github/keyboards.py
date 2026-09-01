from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import STARS_PACKAGES, PREMIUM_PACKAGES


def phone_request_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="📱 Telefon raqamni yuborish", request_contact=True)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⭐ Stars sotib olish", callback_data="menu_stars")
    kb.button(text="💎 Premium sotib olish", callback_data="menu_premium")
    kb.button(text="📦 Mening buyurtmalarim", callback_data="menu_orders")
    kb.adjust(1)
    return kb.as_markup()


def stars_packages_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for pkg in STARS_PACKAGES:
        kb.button(
            text=f"{pkg['title']} — {pkg['price_sum']:,} so'm".replace(",", " "),
            callback_data=f"buy_{pkg['id']}",
        )
    kb.button(text="⬅️ Orqaga", callback_data="back_main")
    kb.adjust(1)
    return kb.as_markup()


def premium_packages_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for pkg in PREMIUM_PACKAGES:
        kb.button(
            text=f"{pkg['title']} — {pkg['price_sum']:,} so'm".replace(",", " "),
            callback_data=f"buy_{pkg['id']}",
        )
    kb.button(text="⬅️ Orqaga", callback_data="back_main")
    kb.adjust(1)
    return kb.as_markup()


def payment_method_kb(product_id: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⭐ Telegram Stars orqali", callback_data=f"pay_stars_{product_id}")
    kb.button(text="💳 Karta orqali", callback_data=f"pay_card_{product_id}")
    kb.button(text="⬅️ Orqaga", callback_data="back_main")
    kb.adjust(1)
    return kb.as_markup()


def admin_order_kb(order_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Tasdiqlash", callback_data=f"admin_confirm_{order_id}")
    kb.button(text="❌ Rad etish", callback_data=f"admin_reject_{order_id}")
    kb.adjust(2)
    return kb.as_markup()


def cancel_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Bekor qilish", callback_data="back_main")
    return kb.as_markup()

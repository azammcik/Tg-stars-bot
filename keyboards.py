from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import STARS_PACKAGES, PREMIUM_PACKAGES
from locales import t


def language_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🇺🇿 O'zbekcha", callback_data="set_lang_uz")
    kb.button(text="🇷🇺 Русский", callback_data="set_lang_ru")
    kb.button(text="🇬🇧 English", callback_data="set_lang_en")
    kb.adjust(1)
    return kb.as_markup()


def phone_request_kb(lang: str = "uz") -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=t("share_phone_btn", lang), request_contact=True)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def main_menu_kb(lang: str = "uz") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t("btn_buy_stars", lang), callback_data="menu_stars")
    kb.button(text=t("btn_buy_premium", lang), callback_data="menu_premium")
    kb.button(text=t("btn_my_orders", lang), callback_data="menu_orders")
    kb.button(text=t("btn_change_lang", lang), callback_data="menu_lang")
    kb.adjust(1)
    return kb.as_markup()


def stars_packages_kb(lang: str = "uz") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    currency = t("currency", lang)
    for pkg in STARS_PACKAGES:
        price = f"{pkg['price_sum']:,}".replace(",", " ")
        kb.button(
            text=f"{pkg['title']} — {price} {currency}",
            callback_data=f"buy_{pkg['id']}",
        )
    kb.button(text=t("btn_back", lang), callback_data="back_main")
    kb.adjust(1)
    return kb.as_markup()


def premium_packages_kb(lang: str = "uz") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    currency = t("currency", lang)
    for pkg in PREMIUM_PACKAGES:
        price = f"{pkg['price_sum']:,}".replace(",", " ")
        kb.button(
            text=f"{pkg['title']} — {price} {currency}",
            callback_data=f"buy_{pkg['id']}",
        )
    kb.button(text=t("btn_back", lang), callback_data="back_main")
    kb.adjust(1)
    return kb.as_markup()


def payment_method_kb(product_id: str, lang: str = "uz") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t("btn_pay_stars", lang), callback_data=f"pay_stars_{product_id}")
    kb.button(text=t("btn_pay_card", lang), callback_data=f"pay_card_{product_id}")
    kb.button(text=t("btn_back", lang), callback_data="back_main")
    kb.adjust(1)
    return kb.as_markup()


def admin_order_kb(order_id: int, lang: str = "uz") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t("btn_admin_confirm", lang), callback_data=f"admin_confirm_{order_id}")
    kb.button(text=t("btn_admin_reject", lang), callback_data=f"admin_reject_{order_id}")
    kb.adjust(2)
    return kb.as_markup()


def cancel_kb(lang: str = "uz") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=t("btn_cancel", lang), callback_data="back_main")
    return kb.as_markup()

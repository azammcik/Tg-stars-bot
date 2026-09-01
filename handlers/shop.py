from aiogram import Router, F
from aiogram.types import CallbackQuery

import database as db
from config import STARS_PACKAGES, PREMIUM_PACKAGES
from keyboards import stars_packages_kb, premium_packages_kb, payment_method_kb, main_menu_kb
from locales import t, get_user_lang

router = Router()


async def _get_lang(user_id: int) -> str:
    user = await db.get_user(user_id)
    return get_user_lang(user)


def find_product(product_id: str):
    for pkg in STARS_PACKAGES + PREMIUM_PACKAGES:
        if pkg["id"] == product_id:
            return pkg
    return None


@router.callback_query(F.data == "menu_stars")
async def show_stars(callback: CallbackQuery):
    lang = await _get_lang(callback.from_user.id)
    await callback.message.edit_text(
        t("choose_stars_package", lang), reply_markup=stars_packages_kb(lang)
    )
    await callback.answer()


@router.callback_query(F.data == "menu_premium")
async def show_premium(callback: CallbackQuery):
    lang = await _get_lang(callback.from_user.id)
    await callback.message.edit_text(
        t("choose_premium_package", lang), reply_markup=premium_packages_kb(lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def choose_product(callback: CallbackQuery):
    lang = await _get_lang(callback.from_user.id)
    product_id = callback.data.removeprefix("buy_")
    product = find_product(product_id)
    if not product:
        await callback.answer(t("product_not_found", lang), show_alert=True)
        return

    price = f"{product['price_sum']:,}".replace(",", " ")
    currency = t("currency", lang)
    price_label = t("price_label", lang)

    await callback.message.edit_text(
        f"🛒 <b>{product['title']}</b>\n"
        f"{price_label}: <b>{price} {currency}</b>\n\n"
        f"{t('choose_payment', lang)}",
        reply_markup=payment_method_kb(product_id, lang),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_orders")
async def show_orders(callback: CallbackQuery):
    lang = await _get_lang(callback.from_user.id)
    orders = await db.get_user_orders(callback.from_user.id)
    if not orders:
        await callback.answer(t("no_orders", lang), show_alert=True)
        return

    status_map = {
        "pending": ("⏳", t("status_pending", lang)),
        "confirmed": ("✅", t("status_confirmed", lang)),
        "rejected": ("❌", t("status_rejected", lang)),
    }
    currency = t("currency", lang)
    lines = [t("your_orders", lang)]
    for o in orders[:15]:
        emoji, status_text = status_map.get(o["status"], ("•", o["status"]))
        price = f"{o['price_sum']:,}".replace(",", " ")
        lines.append(
            f"{emoji} #{o['id']} — {o['product_title']} ({price} {currency}) — {status_text}"
        )

    await callback.message.edit_text("\n".join(lines), reply_markup=main_menu_kb(lang))
    await callback.answer()

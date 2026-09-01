from aiogram import Router, F
from aiogram.types import CallbackQuery

import database as db
from config import STARS_PACKAGES, PREMIUM_PACKAGES
from keyboards import stars_packages_kb, premium_packages_kb, payment_method_kb

router = Router()


def find_product(product_id: str):
    for pkg in STARS_PACKAGES + PREMIUM_PACKAGES:
        if pkg["id"] == product_id:
            return pkg
    return None


@router.callback_query(F.data == "menu_stars")
async def show_stars(callback: CallbackQuery):
    await callback.message.edit_text(
        "⭐ Kerakli Stars paketini tanlang:", reply_markup=stars_packages_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "menu_premium")
async def show_premium(callback: CallbackQuery):
    await callback.message.edit_text(
        "💎 Kerakli Premium muddatini tanlang:", reply_markup=premium_packages_kb()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def choose_product(callback: CallbackQuery):
    product_id = callback.data.removeprefix("buy_")
    product = find_product(product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi.", show_alert=True)
        return

    price = f"{product['price_sum']:,}".replace(",", " ")
    await callback.message.edit_text(
        f"🛒 <b>{product['title']}</b>\n"
        f"Narxi: <b>{price} so'm</b>\n\n"
        f"To'lov usulini tanlang:",
        reply_markup=payment_method_kb(product_id),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_orders")
async def show_orders(callback: CallbackQuery):
    orders = await db.get_user_orders(callback.from_user.id)
    if not orders:
        await callback.answer("Sizda hali buyurtmalar yo'q.", show_alert=True)
        return

    status_emoji = {"pending": "⏳", "confirmed": "✅", "rejected": "❌"}
    lines = ["📦 <b>Sizning buyurtmalaringiz:</b>\n"]
    for o in orders[:15]:
        emoji = status_emoji.get(o["status"], "•")
        price = f"{o['price_sum']:,}".replace(",", " ")
        lines.append(
            f"{emoji} #{o['id']} — {o['product_title']} ({price} so'm) — {o['status']}"
        )

    from keyboards import main_menu_kb

    await callback.message.edit_text("\n".join(lines), reply_markup=main_menu_kb())
    await callback.answer()

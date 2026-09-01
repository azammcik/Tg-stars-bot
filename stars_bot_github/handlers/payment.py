import logging

from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
    Message,
    LabeledPrice,
    PreCheckoutQuery,
)
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

import database as db
from config import STARS_PACKAGES, PREMIUM_PACKAGES, CARD_NUMBER, CARD_HOLDER, ADMIN_IDS
from keyboards import cancel_kb, admin_order_kb, main_menu_kb
from states import CardPayment

router = Router()
logger = logging.getLogger(__name__)


def find_product(product_id: str):
    for pkg in STARS_PACKAGES + PREMIUM_PACKAGES:
        if pkg["id"] == product_id:
            return pkg
    return None


# ---------- Telegram Stars orqali to'lov ----------

@router.callback_query(F.data.startswith("pay_stars_"))
async def pay_with_stars(callback: CallbackQuery, bot: Bot):
    product_id = callback.data.removeprefix("pay_stars_")
    product = find_product(product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi.", show_alert=True)
        return

    # Telegram Stars to'lovlarida narx "XTR" valyutasida, provider_token bo'sh bo'ladi.
    # Eslatma: narxni to'g'ridan-to'g'ri Stars miqdorida belgilash kerak.
    # Bu yerda so'mdagi narxni taxminiy Stars ekvivalentiga o'tkazish o'rniga,
    # admin config.py da har bir mahsulot uchun mos Stars narxini belgilashi tavsiya etiladi.
    stars_price = product.get("stars_price", max(1, product["price_sum"] // 200))

    try:
        await bot.send_invoice(
            chat_id=callback.from_user.id,
            title=product["title"],
            description=f"{product['title']} — botdan xarid",
            payload=f"order_{product_id}",
            provider_token="",  # Stars (XTR) uchun bo'sh qoldiriladi
            currency="XTR",
            prices=[LabeledPrice(label=product["title"], amount=stars_price)],
        )
    except TelegramBadRequest as e:
        logger.error("Invoice yuborishda xatolik: %s", e)
        await callback.message.answer(
            "⚠️ To'lov hisobini yaratib bo'lmadi. Iltimos, birozdan so'ng qayta urinib "
            "ko'ring yoki karta orqali to'lang."
        )
    await callback.answer()


@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot):
    payload = message.successful_payment.invoice_payload
    product_id = payload.removeprefix("order_")
    product = find_product(product_id)
    title = product["title"] if product else product_id

    order_id = await db.create_order(
        user_id=message.from_user.id,
        username=message.from_user.username,
        product_id=product_id,
        product_title=title,
        price_sum=product["price_sum"] if product else 0,
        payment_method="stars",
    )
    await db.set_order_status(order_id, "confirmed")

    await message.answer(
        f"✅ To'lov qabul qilindi! Buyurtma #{order_id} tasdiqlandi.\n"
        f"Tez orada operatorlarimiz buyurtmani tasdiqlashadi!",
        reply_markup=main_menu_kb(),
    )

    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(
                admin_id,
                f"⭐ Yangi Stars to'lovi!\n"
                f"Buyurtma: #{order_id}\n"
                f"Mahsulot: {title}\n"
                f"Foydalanuvchi: @{message.from_user.username or message.from_user.id} "
                f"(ID: {message.from_user.id})",
            )
        except TelegramForbiddenError:
            logger.warning("Admin %s botni bloklagan", admin_id)
        except Exception as e:
            logger.warning("Adminga xabar yuborilmadi: %s", e)


# ---------- Karta orqali qo'lda tasdiqlanadigan to'lov ----------

@router.callback_query(F.data.startswith("pay_card_"))
async def pay_with_card(callback: CallbackQuery, state: FSMContext):
    product_id = callback.data.removeprefix("pay_card_")
    product = find_product(product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi.", show_alert=True)
        return

    price = f"{product['price_sum']:,}".replace(",", " ")

    order_id = await db.create_order(
        user_id=callback.from_user.id,
        username=callback.from_user.username,
        product_id=product_id,
        product_title=product["title"],
        price_sum=product["price_sum"],
        payment_method="card",
    )

    await state.update_data(order_id=order_id)
    await state.set_state(CardPayment.waiting_receipt)

    await callback.message.edit_text(
        f"💳 <b>{product['title']}</b> — {price} so'm\n\n"
        f"To'lovni quyidagi kartaga o'tkazing:\n"
        f"<code>{CARD_NUMBER}</code>\n"
        f"Karta egasi: {CARD_HOLDER}\n\n"
        f"To'lovni amalga oshirgach, chek (screenshot) rasmini shu yerga yuboring.\n"
        f"Buyurtma raqami: <b>#{order_id}</b>",
        reply_markup=cancel_kb(),
    )
    await callback.answer()


@router.message(CardPayment.waiting_receipt, F.photo)
async def receive_receipt(message: Message, state: FSMContext, bot: Bot):
    file_id = message.photo[-1].file_id
    await _process_receipt(message, state, bot, file_id, as_photo=True)


@router.message(CardPayment.waiting_receipt, F.document)
async def receive_receipt_document(message: Message, state: FSMContext, bot: Bot):
    # Screenshot fayl (masalan .jpg/.png hujjat) sifatida yuborilgan bo'lishi mumkin
    mime = message.document.mime_type or ""
    if not mime.startswith("image/"):
        await message.answer(
            "Iltimos, chekning rasmini (screenshot, jpg/png) yuboring 🖼"
        )
        return
    await _process_receipt(message, state, bot, message.document.file_id, as_photo=False)


async def _process_receipt(
    message: Message, state: FSMContext, bot: Bot, file_id: str, as_photo: bool
):
    data = await state.get_data()
    order_id = data.get("order_id")
    if not order_id:
        await message.answer("Xatolik yuz berdi, iltimos qaytadan boshlang: /start")
        await state.clear()
        return

    await db.attach_receipt(order_id, file_id)
    await state.clear()

    order = await db.get_order(order_id)
    user = await db.get_user(message.from_user.id)

    await message.answer(
        f"✅ Chekingiz qabul qilindi!\n"
        f"Buyurtma #{order_id} admin tomonidan tekshiriladi. Tez orada javob olasiz.",
        reply_markup=main_menu_kb(),
    )

    price = f"{order['price_sum']:,}".replace(",", " ")
    phone = user["phone_number"] if user else None
    caption = (
        f"💳 Yangi karta to'lovi!\n"
        f"Buyurtma: #{order_id}\n"
        f"Mahsulot: {order['product_title']}\n"
        f"Narxi: {price} so'm\n"
        f"Foydalanuvchi: @{order['username'] or order['user_id']} "
        f"(ID: {order['user_id']})\n"
        f"Telefon: {phone or '—'}"
    )
    for admin_id in ADMIN_IDS:
        try:
            if as_photo:
                await bot.send_photo(
                    admin_id, photo=file_id, caption=caption, reply_markup=admin_order_kb(order_id)
                )
            else:
                await bot.send_document(
                    admin_id, document=file_id, caption=caption, reply_markup=admin_order_kb(order_id)
                )
        except TelegramForbiddenError:
            logger.warning("Admin %s botni bloklagan", admin_id)
        except Exception as e:
            logger.warning("Adminga chek yuborilmadi: %s", e)


@router.message(CardPayment.waiting_receipt)
async def wrong_content(message: Message):
    await message.answer("Iltimos, to'lov chekining rasmini (screenshot) yuboring 🖼")

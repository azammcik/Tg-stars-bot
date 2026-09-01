from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart

import database as db
from keyboards import main_menu_kb, phone_request_kb

router = Router()

WELCOME_TEXT = (
    "👋 Assalomu alaykum!\n\n"
    "Bu bot orqali siz <b>Telegram Stars</b> va <b>Telegram Premium</b> sotib olishingiz mumkin.\n\n"
    "Kerakli bo'limni tanlang 👇"
)

PHONE_REQUEST_TEXT = (
    "Davom etishdan oldin, iltimos telefon raqamingizni ulashing.\n"
    "Bu buyurtmangiz bilan bog'liq masalalarda siz bilan aloqa qilish uchun kerak. 👇"
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    await db.upsert_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code,
    )

    existing = await db.get_user(user.id)
    if not existing or not existing["phone_number"]:
        await message.answer(PHONE_REQUEST_TEXT, reply_markup=phone_request_kb())
        return

    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb())


@router.message(F.contact)
async def receive_contact(message: Message):
    contact = message.contact
    # Faqat foydalanuvchining o'z raqami qabul qilinadi (boshqa birovning kontaktini
    # forward qilib yuborishining oldini olish uchun)
    if contact.user_id != message.from_user.id:
        await message.answer(
            "Iltimos, faqat o'zingizning telefon raqamingizni yuboring.",
            reply_markup=phone_request_kb(),
        )
        return

    await db.save_phone_number(message.from_user.id, contact.phone_number)
    await message.answer(
        "✅ Rahmat! Endi botdan to'liq foydalanishingiz mumkin.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb())


@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_kb())
    await callback.answer()

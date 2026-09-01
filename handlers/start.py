from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart

import database as db
from keyboards import main_menu_kb, phone_request_kb, language_kb
from locales import t, get_user_lang

router = Router()


async def _get_lang(user_id: int) -> str:
    user = await db.get_user(user_id)
    return get_user_lang(user)


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
    lang = get_user_lang(existing)

    # Agar til hali tanlanmagan bo'lsa (default uz va language_code ham mos kelmasa)
    # Har doim birinchi marta til tanlashni taklif qilamiz agar lang hali default bo'lsa va
    # foydalanuvchi tilni o'zgartirmagan bo'lsa. Oddiyroq: agar phone yo'q bo'lsa til so'raymiz.
    if not existing or not existing["phone_number"]:
        # Avval tilni tanlash
        await message.answer(t("choose_language", "uz"), reply_markup=language_kb())
        return

    await message.answer(t("welcome", lang), reply_markup=main_menu_kb(lang))


@router.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.removeprefix("set_lang_")
    if lang not in ("uz", "ru", "en"):
        lang = "uz"

    await db.set_user_lang(callback.from_user.id, lang)
    await callback.answer()

    # Telefon bormi tekshiramiz
    existing = await db.get_user(callback.from_user.id)
    if not existing or not existing["phone_number"]:
        await callback.message.edit_text(t("lang_changed", lang))
        await callback.message.answer(
            t("phone_request", lang),
            reply_markup=phone_request_kb(lang),
        )
        return

    await callback.message.edit_text(t("lang_changed", lang))
    await callback.message.answer(t("welcome", lang), reply_markup=main_menu_kb(lang))


@router.callback_query(F.data == "menu_lang")
async def change_language(callback: CallbackQuery):
    lang = await _get_lang(callback.from_user.id)
    await callback.message.edit_text(t("choose_language", lang), reply_markup=language_kb())
    await callback.answer()


@router.message(F.contact)
async def receive_contact(message: Message):
    contact = message.contact
    # Faqat foydalanuvchining o'z raqami qabul qilinadi
    if contact.user_id != message.from_user.id:
        lang = await _get_lang(message.from_user.id)
        await message.answer(
            t("phone_only_own", lang),
            reply_markup=phone_request_kb(lang),
        )
        return

    await db.save_phone_number(message.from_user.id, contact.phone_number)
    lang = await _get_lang(message.from_user.id)

    await message.answer(
        t("phone_saved", lang),
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(t("welcome", lang), reply_markup=main_menu_kb(lang))


@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    lang = await _get_lang(callback.from_user.id)
    await callback.message.edit_text(t("welcome", lang), reply_markup=main_menu_kb(lang))
    await callback.answer()

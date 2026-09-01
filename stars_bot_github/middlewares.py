from typing import Any, Awaitable, Callable, Dict
import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

import database as db
from config import ADMIN_IDS
from keyboards import phone_request_kb

logger = logging.getLogger(__name__)

PHONE_REQUEST_TEXT = (
    "⚠️ Davom etish uchun avval telefon raqamingizni ulashishingiz shart.\n\n"
    "Iltimos, pastdagi tugma orqali raqamingizni yuboring 👇"
)


class PhoneRequiredMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = getattr(event, "from_user", None)
        if user is None:
            return await handler(event, data)

        # Adminlar tekshiruvdan ozod
        if user.id in ADMIN_IDS:
            return await handler(event, data)

        # /start buyrug'i va kontakt yuborish har doim ruxsat etiladi
        # (aynan shu ikkisi telefon so'rash oqimini boshlaydi/yakunlaydi)
        if isinstance(event, Message):
            if event.contact is not None:
                return await handler(event, data)
            if event.text and event.text.startswith("/start"):
                return await handler(event, data)

        try:
            db_user = await db.get_user(user.id)
        except Exception as e:
            # Baza vaqtincha ishlamasa ham bot to'xtab qolmasin;
            # xavfsizlik tarafida xatolik — kirishga ruxsat bermaymiz
            logger.error("PhoneRequiredMiddleware DB xatosi: %s", e)
            db_user = None

        if db_user and db_user["phone_number"]:
            return await handler(event, data)

        # Telefon raqami yo'q — bloklaymiz
        if isinstance(event, CallbackQuery):
            await event.answer(
                "Avval telefon raqamingizni ulashing!", show_alert=True
            )
            if event.message:
                await event.message.answer(
                    PHONE_REQUEST_TEXT, reply_markup=phone_request_kb()
                )
        elif isinstance(event, Message):
            await event.answer(PHONE_REQUEST_TEXT, reply_markup=phone_request_kb())

        return None

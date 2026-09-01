from typing import Any, Awaitable, Callable, Dict
import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

import database as db
from config import ADMIN_IDS
from keyboards import phone_request_kb
from locales import t, get_user_lang

logger = logging.getLogger(__name__)


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
        if isinstance(event, Message):
            if event.contact is not None:
                return await handler(event, data)
            if event.text and event.text.startswith("/start"):
                return await handler(event, data)

        # Til tanlash callbacklari ham ruxsat etiladi
        if isinstance(event, CallbackQuery) and event.data and event.data.startswith("set_lang_"):
            return await handler(event, data)

        try:
            db_user = await db.get_user(user.id)
        except Exception as e:
            logger.error("PhoneRequiredMiddleware DB xatosi: %s", e)
            db_user = None

        if db_user and db_user["phone_number"]:
            return await handler(event, data)

        lang = get_user_lang(db_user)

        # Telefon raqami yo'q — bloklaymiz
        if isinstance(event, CallbackQuery):
            await event.answer(t("phone_share_alert", lang), show_alert=True)
            if event.message:
                await event.message.answer(
                    t("phone_request_middleware", lang),
                    reply_markup=phone_request_kb(lang),
                )
        elif isinstance(event, Message):
            await event.answer(
                t("phone_request_middleware", lang),
                reply_markup=phone_request_kb(lang),
            )

        return None

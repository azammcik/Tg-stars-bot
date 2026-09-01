import asyncio
import logging
from logging.handlers import RotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ErrorEvent

from config import BOT_TOKEN
from database import init_db
from handlers import start, shop, payment, admin
from middlewares import PhoneRequiredMiddleware

logger = logging.getLogger(__name__)


def setup_logging():
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 5 MB dan oshsa, eski loglarni almashtiradi (3 ta zaxira nusxa bilan)
    file_handler = RotatingFileHandler(
        "bot.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(console_handler)
    root.addHandler(file_handler)

    # aiogram'ning haddan tashqari batafsil (DEBUG) loglarini kamaytiramiz
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)


async def main():
    setup_logging()

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN topilmadi. .env faylini yarating va uni to'ldiring "
            "(.env.example faylidan nusxa oling)."
        )

    await init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(PhoneRequiredMiddleware())
    dp.callback_query.middleware(PhoneRequiredMiddleware())

    dp.include_router(start.router)
    dp.include_router(shop.router)
    dp.include_router(payment.router)
    dp.include_router(admin.router)

    @dp.errors()
    async def global_error_handler(event: ErrorEvent):
        # Har qanday kutilmagan xatolik botni to'xtatmasligi uchun shu yerda ushlanadi
        logger.exception(
            "Yangilanishni qayta ishlashda xatolik: %s | update=%s",
            event.exception,
            event.update,
        )
        return True

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot ishga tushdi (polling rejimida)")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot to'xtatildi")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot foydalanuvchi tomonidan to'xtatildi")

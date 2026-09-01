# -*- coding: utf-8 -*-
"""
Bot matnlari — 3 til: uz (O'zbek), ru (Русский), en (English)
"""

TEXTS = {
    # ========== LANGUAGE SELECTION ==========
    "choose_language": {
        "uz": "🌐 Tilni tanlang / Выберите язык / Choose language:",
        "ru": "🌐 Tilni tanlang / Выберите язык / Choose language:",
        "en": "🌐 Tilni tanlang / Выберите язык / Choose language:",
    },
    "lang_changed": {
        "uz": "✅ Til o'zgartirildi: O'zbekcha",
        "ru": "✅ Язык изменён: Русский",
        "en": "✅ Language changed: English",
    },

    # ========== START / WELCOME ==========
    "welcome": {
        "uz": (
            "👋 Assalomu alaykum!\n\n"
            "Bu bot orqali siz <b>Telegram Stars</b> va <b>Telegram Premium</b> sotib olishingiz mumkin.\n\n"
            "Kerakli bo'limni tanlang 👇"
        ),
        "ru": (
            "👋 Здравствуйте!\n\n"
            "С помощью этого бота вы можете купить <b>Telegram Stars</b> и <b>Telegram Premium</b>.\n\n"
            "Выберите нужный раздел 👇"
        ),
        "en": (
            "👋 Hello!\n\n"
            "With this bot you can buy <b>Telegram Stars</b> and <b>Telegram Premium</b>.\n\n"
            "Choose a section 👇"
        ),
    },
    "phone_request": {
        "uz": (
            "Davom etishdan oldin, iltimos telefon raqamingizni ulashing.\n"
            "Bu buyurtmangiz bilan bog'liq masalalarda siz bilan aloqa qilish uchun kerak. 👇"
        ),
        "ru": (
            "Перед продолжением, пожалуйста, поделитесь номером телефона.\n"
            "Это нужно для связи с вами по вопросам заказа. 👇"
        ),
        "en": (
            "Before continuing, please share your phone number.\n"
            "This is needed to contact you regarding your order. 👇"
        ),
    },
    "phone_request_middleware": {
        "uz": (
            "⚠️ Davom etish uchun avval telefon raqamingizni ulashishingiz shart.\n\n"
            "Iltimos, pastdagi tugma orqali raqamingizni yuboring 👇"
        ),
        "ru": (
            "⚠️ Для продолжения необходимо поделиться номером телефона.\n\n"
            "Пожалуйста, отправьте номер с помощью кнопки ниже 👇"
        ),
        "en": (
            "⚠️ To continue, you must share your phone number first.\n\n"
            "Please send your number using the button below 👇"
        ),
    },
    "phone_only_own": {
        "uz": "Iltimos, faqat o'zingizning telefon raqamingizni yuboring.",
        "ru": "Пожалуйста, отправьте только свой номер телефона.",
        "en": "Please send only your own phone number.",
    },
    "phone_saved": {
        "uz": "✅ Rahmat! Endi botdan to'liq foydalanishingiz mumkin.",
        "ru": "✅ Спасибо! Теперь вы можете полноценно пользоваться ботом.",
        "en": "✅ Thank you! You can now fully use the bot.",
    },
    "share_phone_btn": {
        "uz": "📱 Telefon raqamni yuborish",
        "ru": "📱 Отправить номер телефона",
        "en": "📱 Share phone number",
    },

    # ========== MAIN MENU ==========
    "btn_buy_stars": {
        "uz": "⭐ Stars sotib olish",
        "ru": "⭐ Купить Stars",
        "en": "⭐ Buy Stars",
    },
    "btn_buy_premium": {
        "uz": "💎 Premium sotib olish",
        "ru": "💎 Buy Premium",
        "en": "💎 Buy Premium",
    },
    "btn_my_orders": {
        "uz": "📦 Mening buyurtmalarim",
        "ru": "📦 Мои заказы",
        "en": "📦 My orders",
    },
    "btn_change_lang": {
        "uz": "🌐 Tilni o'zgartirish",
        "ru": "🌐 Сменить язык",
        "en": "🌐 Change language",
    },
    "btn_back": {
        "uz": "⬅️ Orqaga",
        "ru": "⬅️ Назад",
        "en": "⬅️ Back",
    },
    "btn_cancel": {
        "uz": "⬅️ Bekor qilish",
        "ru": "⬅️ Отмена",
        "en": "⬅️ Cancel",
    },

    # ========== SHOP ==========
    "choose_stars_package": {
        "uz": "⭐ Kerakli Stars paketini tanlang:",
        "ru": "⭐ Выберите нужный пакет Stars:",
        "en": "⭐ Choose a Stars package:",
    },
    "choose_premium_package": {
        "uz": "💎 Kerakli Premium muddatini tanlang:",
        "ru": "💎 Выберите срок Premium:",
        "en": "💎 Choose a Premium period:",
    },
    "product_not_found": {
        "uz": "Mahsulot topilmadi.",
        "ru": "Товар не найден.",
        "en": "Product not found.",
    },
    "choose_payment": {
        "uz": "To'lov usulini tanlang:",
        "ru": "Выберите способ оплаты:",
        "en": "Choose a payment method:",
    },
    "price_label": {
        "uz": "Narxi",
        "ru": "Цена",
        "en": "Price",
    },
    "currency": {
        "uz": "so'm",
        "ru": "сум",
        "en": "UZS",
    },
    "btn_pay_stars": {
        "uz": "⭐ Telegram Stars orqali",
        "ru": "⭐ Через Telegram Stars",
        "en": "⭐ Via Telegram Stars",
    },
    "btn_pay_card": {
        "uz": "💳 Karta orqali",
        "ru": "💳 Банковской картой",
        "en": "💳 By card",
    },
    "no_orders": {
        "uz": "Sizda hali buyurtmalar yo'q.",
        "ru": "У вас пока нет заказов.",
        "en": "You have no orders yet.",
    },
    "your_orders": {
        "uz": "📦 <b>Sizning buyurtmalaringiz:</b>\n",
        "ru": "📦 <b>Ваши заказы:</b>\n",
        "en": "📦 <b>Your orders:</b>\n",
    },
    "status_pending": {
        "uz": "kutilmoqda",
        "ru": "ожидание",
        "en": "pending",
    },
    "status_confirmed": {
        "uz": "tasdiqlangan",
        "ru": "подтверждён",
        "en": "confirmed",
    },
    "status_rejected": {
        "uz": "rad etilgan",
        "ru": "отклонён",
        "en": "rejected",
    },

    # ========== PAYMENT ==========
    "invoice_description": {
        "uz": "{title} — botdan xarid",
        "ru": "{title} — покупка в боте",
        "en": "{title} — purchase via bot",
    },
    "invoice_error": {
        "uz": (
            "⚠️ To'lov hisobini yaratib bo'lmadi. Iltimos, birozdan so'ng qayta urinib "
            "ko'ring yoki karta orqali to'lang."
        ),
        "ru": (
            "⚠️ Не удалось создать счёт. Пожалуйста, попробуйте позже "
            "или оплатите картой."
        ),
        "en": (
            "⚠️ Failed to create invoice. Please try again later "
            "or pay by card."
        ),
    },
    "payment_success": {
        "uz": (
            "✅ To'lov qabul qilindi! Buyurtma #{order_id} tasdiqlandi.\n"
            "Tez orada mahsulot yetkazib beriladi."
        ),
        "ru": (
            "✅ Оплата принята! Заказ #{order_id} подтверждён.\n"
            "Товар будет доставлен в ближайшее время."
        ),
        "en": (
            "✅ Payment received! Order #{order_id} confirmed.\n"
            "The product will be delivered soon."
        ),
    },
    "card_payment_info": {
        "uz": (
            "💳 <b>{title}</b> — {price} so'm\n\n"
            "To'lovni quyidagi kartaga o'tkazing:\n"
            "<code>{card}</code>\n"
            "Karta egasi: {holder}\n\n"
            "To'lovni amalga oshirgach, chek (screenshot) rasmini shu yerga yuboring.\n"
            "Buyurtma raqami: <b>#{order_id}</b>"
        ),
        "ru": (
            "💳 <b>{title}</b> — {price} сум\n\n"
            "Переведите оплату на следующую карту:\n"
            "<code>{card}</code>\n"
            "Владелец карты: {holder}\n\n"
            "После оплаты отправьте сюда скриншот чека.\n"
            "Номер заказа: <b>#{order_id}</b>"
        ),
        "en": (
            "💳 <b>{title}</b> — {price} UZS\n\n"
            "Transfer the payment to the following card:\n"
            "<code>{card}</code>\n"
            "Card holder: {holder}\n\n"
            "After payment, send a screenshot of the receipt here.\n"
            "Order number: <b>#{order_id}</b>"
        ),
    },
    "receipt_received": {
        "uz": (
            "✅ Chekingiz qabul qilindi!\n"
            "Buyurtma #{order_id} admin tomonidan tekshiriladi. Tez orada javob olasiz."
        ),
        "ru": (
            "✅ Чек получен!\n"
            "Заказ #{order_id} будет проверен администратором. Скоро вы получите ответ."
        ),
        "en": (
            "✅ Receipt received!\n"
            "Order #{order_id} will be checked by an admin. You will get a response soon."
        ),
    },
    "send_receipt_photo": {
        "uz": "Iltimos, chekning rasmini (screenshot, jpg/png) yuboring 🖼",
        "ru": "Пожалуйста, отправьте фото чека (скриншот, jpg/png) 🖼",
        "en": "Please send a photo of the receipt (screenshot, jpg/png) 🖼",
    },
    "send_receipt_only": {
        "uz": "Iltimos, to'lov chekining rasmini (screenshot) yuboring 🖼",
        "ru": "Пожалуйста, отправьте фото чека об оплате (скриншот) 🖼",
        "en": "Please send a photo of the payment receipt (screenshot) 🖼",
    },
    "error_restart": {
        "uz": "Xatolik yuz berdi, iltimos qaytadan boshlang: /start",
        "ru": "Произошла ошибка, пожалуйста, начните заново: /start",
        "en": "An error occurred, please start again: /start",
    },
    "order_confirmed_user": {
        "uz": "✅ Buyurtmangiz #{order_id} tasdiqlandi! Tez orada mahsulot yetkaziladi.",
        "ru": "✅ Ваш заказ #{order_id} подтверждён! Товар будет доставлен в ближайшее время.",
        "en": "✅ Your order #{order_id} has been confirmed! The product will be delivered soon.",
    },
    "order_rejected_user": {
        "uz": "❌ Buyurtmangiz #{order_id} rad etildi. Savollar bo'lsa, admin bilan bog'laning.",
        "ru": "❌ Ваш заказ #{order_id} отклонён. Если есть вопросы — свяжитесь с админом.",
        "en": "❌ Your order #{order_id} has been rejected. Contact the admin if you have questions.",
    },

    # ========== ADMIN (keep mostly Uzbek, but add basic) ==========
    "admin_no_permission": {
        "uz": "Ruxsat yo'q.",
        "ru": "Нет доступа.",
        "en": "No permission.",
    },
    "admin_order_not_found": {
        "uz": "Buyurtma topilmadi.",
        "ru": "Заказ не найден.",
        "en": "Order not found.",
    },
    "admin_already_processed": {
        "uz": "Bu buyurtma allaqachon '{status}' holatida.",
        "ru": "Этот заказ уже в статусе '{status}'.",
        "en": "This order is already in '{status}' status.",
    },
    "admin_confirmed": {
        "uz": "Tasdiqlandi!",
        "ru": "Подтверждено!",
        "en": "Confirmed!",
    },
    "admin_rejected": {
        "uz": "Rad etildi!",
        "ru": "Отклонено!",
        "en": "Rejected!",
    },
    "btn_admin_confirm": {
        "uz": "✅ Tasdiqlash",
        "ru": "✅ Подтвердить",
        "en": "✅ Confirm",
    },
    "btn_admin_reject": {
        "uz": "❌ Rad etish",
        "ru": "❌ Отклонить",
        "en": "❌ Reject",
    },
    "phone_share_alert": {
        "uz": "Avval telefon raqamingizni ulashing!",
        "ru": "Сначала поделитесь номером телефона!",
        "en": "Share your phone number first!",
    },
}


def t(key: str, lang: str = "uz", **kwargs) -> str:
    """Get translated text by key and language."""
    lang = lang if lang in ("uz", "ru", "en") else "uz"
    text = TEXTS.get(key, {}).get(lang) or TEXTS.get(key, {}).get("uz") or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text


def get_user_lang(user_row) -> str:
    """Extract language from DB user row. Defaults to 'uz'."""
    if user_row is None:
        return "uz"
    lang = user_row["lang"] if "lang" in user_row.keys() else None
    if not lang:
        # fallback to Telegram language_code
        code = user_row["language_code"] if "language_code" in user_row.keys() else None
        if code:
            code = code.lower()
            if code.startswith("ru"):
                return "ru"
            if code.startswith("en"):
                return "en"
        return "uz"
    return lang if lang in ("uz", "ru", "en") else "uz"

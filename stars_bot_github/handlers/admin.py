import csv
import io
import os
import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, BufferedInputFile, FSInputFile
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

import database as db
from config import ADMIN_IDS, DB_PATH

router = Router()
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


HELP_TEXT = (
    "🛠 <b>Admin buyruqlari</b>\n\n"
    "/admin — kutilayotgan buyurtmalar ro'yxati\n"
    "/confirm ID — buyurtmani tasdiqlash\n"
    "/reject ID — buyurtmani rad etish\n"
    "/users — barcha foydalanuvchilar ro'yxati\n"
    "/user ID — bitta foydalanuvchi haqida to'liq ma'lumot\n"
    "/stats — bot bo'yicha umumiy statistika\n"
    "/export — foydalanuvchilar ro'yxatini CSV fayl sifatida yuklab olish\n"
    "/backup — bazaning (bot.db) to'liq nusxasini fayl sifatida yuklab olish\n"
    "/broadcast matn — barcha foydalanuvchilarga xabar yuborish"
)


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    pending = await db.get_pending_orders()
    if not pending:
        await message.answer("✅ Hozircha kutilayotgan buyurtmalar yo'q.\n\n" + HELP_TEXT)
        return

    lines = ["⏳ <b>Kutilayotgan buyurtmalar:</b>\n"]
    for o in pending:
        price = f"{o['price_sum']:,}".replace(",", " ")
        lines.append(
            f"#{o['id']} — {o['product_title']} ({price} so'm) — "
            f"@{o['username'] or o['user_id']} — {o['payment_method']}"
        )
    lines.append("\n" + HELP_TEXT)
    await message.answer("\n".join(lines))


@router.message(Command("help"))
async def admin_help(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer(HELP_TEXT)


@router.message(Command("stats"))
async def stats_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return

    s = await db.get_stats()
    revenue = f"{s['total_revenue']:,}".replace(",", " ")
    text = (
        "📊 <b>Bot statistikasi</b>\n\n"
        f"👥 Jami foydalanuvchilar: {s['total_users']}\n"
        f"📱 Telefon ulashganlar: {s['users_with_phone']}\n\n"
        f"✅ Tasdiqlangan buyurtmalar: {s['confirmed_orders']}\n"
        f"⏳ Kutilayotgan buyurtmalar: {s['pending_orders']}\n"
        f"❌ Rad etilgan buyurtmalar: {s['rejected_orders']}\n\n"
        f"💰 Jami tushum: {revenue} so'm"
    )
    await message.answer(text)


@router.message(Command("users"))
async def list_users(message: Message):
    if not is_admin(message.from_user.id):
        return

    users = await db.get_all_users()
    if not users:
        await message.answer("Hozircha foydalanuvchilar yo'q.")
        return

    lines = [f"👥 <b>Jami foydalanuvchilar: {len(users)}</b>\n"]
    for u in users[:50]:
        name = " ".join(filter(None, [u["first_name"], u["last_name"]])) or "—"
        username = f"@{u['username']}" if u["username"] else "—"
        phone = u["phone_number"] or "—"
        lines.append(
            f"• ID: <code>{u['user_id']}</code> | {name} | {username} | 📱 {phone}"
        )
    if len(users) > 50:
        lines.append(f"\n... va yana {len(users) - 50} ta.")
        lines.append("To'liq ro'yxat uchun: /export")
    lines.append("\nBatafsil ma'lumot uchun: /user ID")

    await message.answer("\n".join(lines))


@router.message(Command("export"))
async def export_users(message: Message):
    if not is_admin(message.from_user.id):
        return

    users = await db.get_all_users()
    if not users:
        await message.answer("Hozircha foydalanuvchilar yo'q.")
        return

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["user_id", "username", "first_name", "last_name", "phone_number",
         "language_code", "first_seen", "last_seen"]
    )
    for u in users:
        writer.writerow(
            [u["user_id"], u["username"], u["first_name"], u["last_name"],
             u["phone_number"], u["language_code"], u["first_seen"], u["last_seen"]]
        )

    file_bytes = buffer.getvalue().encode("utf-8-sig")  # Excel'da to'g'ri ochilishi uchun
    file = BufferedInputFile(file_bytes, filename="users_export.csv")
    await message.answer_document(file, caption=f"👥 Jami {len(users)} ta foydalanuvchi")


@router.message(Command("backup"))
async def backup_db(message: Message):
    if not is_admin(message.from_user.id):
        return

    if not os.path.exists(DB_PATH):
        await message.answer(f"⚠️ Baza fayli topilmadi: {DB_PATH}")
        return

    try:
        file = FSInputFile(DB_PATH, filename="bot.db")
        await message.answer_document(
            file,
            caption=(
                "🗄 Bazaning to'liq nusxasi (bot.db).\n\n"
                "Bu faylni SQLite ochuvchi dastur bilan (masalan DB Browser for SQLite) "
                "kompyuteringizda ochishingiz mumkin."
            ),
        )
    except Exception as e:
        logger.error("Backup yuborishda xatolik: %s", e)
        await message.answer(f"⚠️ Bazani yuborishda xatolik yuz berdi: {e}")


@router.message(Command("broadcast"))
async def broadcast_cmd(message: Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return

    text = message.text.removeprefix("/broadcast").strip()
    if not text:
        await message.answer(
            "Foydalanish: /broadcast Xabar matni\n\n"
            "Bu buyruq barcha foydalanuvchilarga xabar yuboradi."
        )
        return

    users = await db.get_all_users()
    status_msg = await message.answer(f"📤 Yuborilmoqda... (0/{len(users)})")

    sent, failed = 0, 0
    for i, u in enumerate(users, start=1):
        try:
            await bot.send_message(u["user_id"], text)
            sent += 1
        except TelegramForbiddenError:
            await db.set_user_blocked(u["user_id"], True)
            failed += 1
        except Exception as e:
            logger.warning("Broadcast xatosi (user %s): %s", u["user_id"], e)
            failed += 1

        if i % 25 == 0:
            try:
                await status_msg.edit_text(f"📤 Yuborilmoqda... ({i}/{len(users)})")
            except TelegramBadRequest:
                pass

    await status_msg.edit_text(
        f"✅ Xabar yuborish yakunlandi.\n\nYuborildi: {sent}\nXato/bloklangan: {failed}"
    )


@router.message(Command("confirm"))
async def confirm_order_cmd(message: Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return
    await _confirm_order(message, bot)


@router.message(Command("reject"))
async def reject_order_cmd(message: Message, bot: Bot):
    if not is_admin(message.from_user.id):
        return
    await _reject_order(message, bot)


async def _confirm_order(message: Message, bot: Bot):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Foydalanish: /confirm ID")
        return
    order_id = int(parts[1])
    order = await db.get_order(order_id)
    if not order:
        await message.answer("Buyurtma topilmadi.")
        return
    if order["status"] != "pending":
        await message.answer(f"⚠️ Buyurtma #{order_id} allaqachon '{order['status']}' holatida.")
        return

    await db.set_order_status(order_id, "confirmed")
    await message.answer(f"✅ Buyurtma #{order_id} tasdiqlandi.")
    try:
        await bot.send_message(
            order["user_id"],
            f"✅ Buyurtmangiz #{order_id} tasdiqlandi! Tez orada mahsulot yetkaziladi.",
        )
    except TelegramForbiddenError:
        await db.set_user_blocked(order["user_id"], True)
    except Exception as e:
        logger.warning("Foydalanuvchiga xabar yuborilmadi (order %s): %s", order_id, e)


async def _reject_order(message: Message, bot: Bot):
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Foydalanish: /reject ID")
        return
    order_id = int(parts[1])
    order = await db.get_order(order_id)
    if not order:
        await message.answer("Buyurtma topilmadi.")
        return
    if order["status"] != "pending":
        await message.answer(f"⚠️ Buyurtma #{order_id} allaqachon '{order['status']}' holatida.")
        return

    await db.set_order_status(order_id, "rejected")
    await message.answer(f"❌ Buyurtma #{order_id} rad etildi.")
    try:
        await bot.send_message(
            order["user_id"],
            f"❌ Buyurtmangiz #{order_id} rad etildi. Savollar bo'lsa, admin bilan bog'laning.",
        )
    except TelegramForbiddenError:
        await db.set_user_blocked(order["user_id"], True)
    except Exception as e:
        logger.warning("Foydalanuvchiga xabar yuborilmadi (order %s): %s", order_id, e)


@router.message(Command("user"))
async def user_detail(message: Message):
    if not is_admin(message.from_user.id):
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Foydalanish: /user ID")
        return

    user = await db.get_user(int(parts[1]))
    if not user:
        await message.answer("Foydalanuvchi topilmadi.")
        return

    orders = await db.get_user_orders(user["user_id"])
    orders_count = len(orders)
    confirmed_count = sum(1 for o in orders if o["status"] == "confirmed")
    total_spent = sum(o["price_sum"] for o in orders if o["status"] == "confirmed")

    name = " ".join(filter(None, [user["first_name"], user["last_name"]])) or "—"
    username = f"@{user['username']}" if user["username"] else "—"
    blocked_note = "\n🚫 Botni bloklagan" if user["is_blocked"] else ""

    text = (
        f"👤 <b>Foydalanuvchi ma'lumotlari</b>\n\n"
        f"ID: <code>{user['user_id']}</code>\n"
        f"Ism: {name}\n"
        f"Username: {username}\n"
        f"Til: {user['language_code'] or '—'}\n"
        f"Telefon: {user['phone_number'] or 'ulashilmagan'}\n"
        f"Birinchi murojaat: {user['first_seen']}\n"
        f"Oxirgi faollik: {user['last_seen']}"
        f"{blocked_note}\n\n"
        f"📦 Buyurtmalar: {orders_count} (tasdiqlangan: {confirmed_count})\n"
        f"💰 Jami xarid: {total_spent:,} so'm".replace(",", " ")
    )
    await message.answer(text)


# Admin xabaridagi tugmalar orqali tasdiqlash/rad etish
@router.callback_query(F.data.startswith("admin_confirm_"))
async def confirm_via_button(callback: CallbackQuery, bot: Bot):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return
    order_id = int(callback.data.removeprefix("admin_confirm_"))
    order = await db.get_order(order_id)
    if not order:
        await callback.answer("Buyurtma topilmadi.", show_alert=True)
        return
    if order["status"] != "pending":
        await callback.answer(f"Bu buyurtma allaqachon '{order['status']}' holatida.", show_alert=True)
        return

    await db.set_order_status(order_id, "confirmed")
    try:
        await callback.message.edit_caption(
            caption=(callback.message.caption or "") + "\n\n✅ TASDIQLANDI"
        )
    except TelegramBadRequest:
        pass
    try:
        await bot.send_message(
            order["user_id"],
            f"✅ Buyurtmangiz #{order_id} tasdiqlandi! Tez orada mahsulot yetkaziladi.",
        )
    except TelegramForbiddenError:
        await db.set_user_blocked(order["user_id"], True)
    except Exception as e:
        logger.warning("Foydalanuvchiga xabar yuborilmadi (order %s): %s", order_id, e)
    await callback.answer("Tasdiqlandi!")


@router.callback_query(F.data.startswith("admin_reject_"))
async def reject_via_button(callback: CallbackQuery, bot: Bot):
    if not is_admin(callback.from_user.id):
        await callback.answer("Ruxsat yo'q.", show_alert=True)
        return
    order_id = int(callback.data.removeprefix("admin_reject_"))
    order = await db.get_order(order_id)
    if not order:
        await callback.answer("Buyurtma topilmadi.", show_alert=True)
        return
    if order["status"] != "pending":
        await callback.answer(f"Bu buyurtma allaqachon '{order['status']}' holatida.", show_alert=True)
        return

    await db.set_order_status(order_id, "rejected")
    try:
        await callback.message.edit_caption(
            caption=(callback.message.caption or "") + "\n\n❌ RAD ETILDI"
        )
    except TelegramBadRequest:
        pass
    try:
        await bot.send_message(
            order["user_id"],
            f"❌ Buyurtmangiz #{order_id} rad etildi. Savollar bo'lsa, admin bilan bog'laning.",
        )
    except TelegramForbiddenError:
        await db.set_user_blocked(order["user_id"], True)
    except Exception as e:
        logger.warning("Foydalanuvchiga xabar yuborilmadi (order %s): %s", order_id, e)
    await callback.answer("Rad etildi!")

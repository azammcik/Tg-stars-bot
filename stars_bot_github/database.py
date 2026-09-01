import aiosqlite
import logging
from datetime import datetime
from config import DB_PATH

logger = logging.getLogger(__name__)

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT,
    product_id TEXT NOT NULL,
    product_title TEXT NOT NULL,
    price_sum INTEGER NOT NULL,
    payment_method TEXT NOT NULL,      -- 'stars' yoki 'card'
    status TEXT NOT NULL DEFAULT 'pending',  -- pending / confirmed / rejected
    receipt_file_id TEXT,
    created_at TEXT NOT NULL
);
"""

CREATE_ORDERS_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);",
    "CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);",
]

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    language_code TEXT,
    phone_number TEXT,
    is_blocked INTEGER NOT NULL DEFAULT 0,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL
);
"""


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # WAL rejimi — bir vaqtda o'qish/yozish tezligini va barqarorligini oshiradi
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute("PRAGMA foreign_keys=ON;")
        await db.execute(CREATE_ORDERS_TABLE)
        await db.execute(CREATE_USERS_TABLE)
        for idx in CREATE_ORDERS_INDEXES:
            await db.execute(idx)
        await db.commit()
    logger.info("Ma'lumotlar bazasi tayyor: %s", DB_PATH)


async def upsert_user(
    user_id: int,
    username: str | None,
    first_name: str | None = None,
    last_name: str | None = None,
    language_code: str | None = None,
):
    now = datetime.utcnow().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO users (user_id, username, first_name, last_name, language_code,
                                first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username,
                first_name=excluded.first_name,
                last_name=excluded.last_name,
                language_code=excluded.language_code,
                last_seen=excluded.last_seen
            """,
            (user_id, username, first_name, last_name, language_code, now, now),
        )
        await db.commit()


async def save_phone_number(user_id: int, phone_number: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET phone_number = ? WHERE user_id = ?",
            (phone_number, user_id),
        )
        await db.commit()


async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return await cursor.fetchone()


async def get_all_users():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM users ORDER BY first_seen DESC")
        return await cursor.fetchall()


async def set_user_blocked(user_id: int, blocked: bool):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET is_blocked = ? WHERE user_id = ?",
            (1 if blocked else 0, user_id),
        )
        await db.commit()


async def get_stats():
    """Bot bo'yicha umumiy statistika: adminga tezkor ko'rinish uchun."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("SELECT COUNT(*) AS c FROM users")
        total_users = (await cursor.fetchone())["c"]

        cursor = await db.execute(
            "SELECT COUNT(*) AS c FROM users WHERE phone_number IS NOT NULL"
        )
        users_with_phone = (await cursor.fetchone())["c"]

        cursor = await db.execute(
            "SELECT COUNT(*) AS c, COALESCE(SUM(price_sum), 0) AS s "
            "FROM orders WHERE status = 'confirmed'"
        )
        row = await cursor.fetchone()
        confirmed_orders, total_revenue = row["c"], row["s"]

        cursor = await db.execute(
            "SELECT COUNT(*) AS c FROM orders WHERE status = 'pending'"
        )
        pending_orders = (await cursor.fetchone())["c"]

        cursor = await db.execute(
            "SELECT COUNT(*) AS c FROM orders WHERE status = 'rejected'"
        )
        rejected_orders = (await cursor.fetchone())["c"]

        return {
            "total_users": total_users,
            "users_with_phone": users_with_phone,
            "confirmed_orders": confirmed_orders,
            "pending_orders": pending_orders,
            "rejected_orders": rejected_orders,
            "total_revenue": total_revenue,
        }


async def create_order(
    user_id: int,
    username: str | None,
    product_id: str,
    product_title: str,
    price_sum: int,
    payment_method: str,
) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO orders (user_id, username, product_id, product_title, price_sum,
                                 payment_method, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
            """,
            (
                user_id,
                username,
                product_id,
                product_title,
                price_sum,
                payment_method,
                datetime.utcnow().isoformat(),
            ),
        )
        await db.commit()
        return cursor.lastrowid


async def attach_receipt(order_id: int, file_id: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE orders SET receipt_file_id = ? WHERE id = ?", (file_id, order_id)
        )
        await db.commit()


async def set_order_status(order_id: int, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE orders SET status = ? WHERE id = ?", (status, order_id)
        )
        await db.commit()


async def get_order(order_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        return await cursor.fetchone()


async def get_user_orders(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC", (user_id,)
        )
        return await cursor.fetchall()


async def get_pending_orders():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM orders WHERE status = 'pending' ORDER BY id ASC"
        )
        return await cursor.fetchall()

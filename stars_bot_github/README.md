# Stars & Premium sotuvchi Telegram bot

Telegram Stars va Telegram Premium sotadigan bot. `aiogram 3` + `SQLite` asosida yozilgan.
Ikkita to'lov usulini qo'llab-quvvatlaydi:

- ⭐ **Telegram Stars (XTR)** — rasmiy Telegram to'lov tizimi orqali, avtomatik tasdiqlanadi
- 💳 **Karta orqali** — foydalanuvchi kartaga pul o'tkazadi, chek yuboradi, admin qo'lda tasdiqlaydi

## 1. O'rnatish

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Sozlash

1. [@BotFather](https://t.me/BotFather) orqali yangi bot yarating, tokenni oling.
2. [@userinfobot](https://t.me/userinfobot) orqali o'zingizning Telegram ID'ingizni bilib oling (admin sifatida).
3. `.env.example` faylidan nusxa ko'chiring:

```bash
cp .env.example .env
```

4. `.env` faylini oching va to'ldiring:

```
BOT_TOKEN=sizning_bot_tokeningiz
ADMIN_IDS=sizning_telegram_id
CARD_NUMBER=8600 1234 5678 9012
CARD_HOLDER=Ism Familiya
```

5. `config.py` faylida `STARS_PACKAGES` va `PREMIUM_PACKAGES` ro'yxatlarini o'z narxlaringiz bilan
   moslashtiring. Har bir mahsulotga ixtiyoriy ravishda `"stars_price"` (Stars to'lovi uchun XTR
   miqdori) qo'shishingiz mumkin — aks holda narx so'mdan taxminiy hisoblanadi.

## 3. Ishga tushirish

```bash
python bot.py
```

## 4. Qanday ishlaydi

- Foydalanuvchi `/start` bosadi → mahsulot turini (Stars/Premium) tanlaydi → paketni tanlaydi →
  to'lov usulini tanlaydi.
- **Stars orqali** to'langanda — Telegram o'zi to'lovni tasdiqlaydi, buyurtma avtomatik
  "confirmed" holatiga o'tadi va admin xabardor qilinadi.
- **Karta orqali** to'langanda — foydalanuvchiga karta raqami ko'rsatiladi, u chek (screenshot)
  yuboradi, buyurtma "pending" holatida saqlanadi va admin(lar)ga chek + tasdiqlash/rad etish
  tugmalari bilan xabar yuboriladi.
- Admin buyurtmani tugma orqali yoki `/confirm <ID>` / `/reject <ID>` buyruqlari bilan
  tasdiqlaydi/rad etadi. Foydalanuvchiga avtomatik xabar boradi. Bir marta tasdiqlangan/rad
  etilgan buyurtma qayta o'zgartirilmaydi (himoya bor).
- `/admin` buyrug'i — barcha kutilayotgan buyurtmalar ro'yxatini ko'rsatadi.
- `/stats` — jami foydalanuvchilar, telefon ulashganlar soni, tasdiqlangan/kutilayotgan/rad
  etilgan buyurtmalar va jami tushum.
- `/export` — barcha foydalanuvchilarni CSV fayl sifatida yuklab olish (Excel'da ochiladi).
- `/broadcast <matn>` — barcha foydalanuvchilarga bir vaqtda xabar yuborish. Botni bloklagan
  foydalanuvchilar avtomatik aniqlanadi va belgilab qo'yiladi.
- `/help` — admin buyruqlari ro'yxati.

## 5. Foydalanuvchi ma'lumotlari

Bot endi har bir foydalanuvchi haqida quyidagi ma'lumotlarni yig'adi va saqlaydi:

- Telegram ID, username, ism-familiya, til kodi — `/start` bosilganda avtomatik olinadi
- Telefon raqami — birinchi marta botga kirganda "📱 Telefon raqamni yuborish" tugmasi orqali
  so'raladi (faqat foydalanuvchining o'z raqami qabul qilinadi). **Bu majburiy** — telefon
  ulashilmaguncha boshqa hech qanday tugma yoki buyruq ishlamaydi (`middlewares.py` orqali
  ta'minlangan). Adminlar (`ADMIN_IDS`) bu tekshiruvdan ozod.
- Birinchi va oxirgi faollik vaqti

Admin buyruqlari:

- `/users` — barcha foydalanuvchilar ro'yxati (ID, ism, username, telefon)
- `/user <ID>` — bitta foydalanuvchi haqida to'liq ma'lumot: aloqa ma'lumotlari, buyurtmalar
  soni va jami xarid summasi

**Muhim cheklov:** Telegram Bot API foydalanuvchining hisobi qachon yaratilganini, elektron
pochtasini, joylashuvini (agar u o'zi yubormasa) yoki boshqa botlar/kanallardagi faolligini
umuman taqdim etmaydi — bular Telegram tomonidan botlarga ochiq qilinmagan. Shu sababli bu
ma'lumotlar bazaga qo'shilmadi. Agar yashash manzili yoki boshqa qo'shimcha ma'lumot kerak
bo'lsa, buni faqat foydalanuvchining o'zidan so'rab olish mumkin (masalan, buyurtma jarayonida
matnli xabar orqali).

**Maxfiylik eslatmasi:** telefon raqami va shaxsiy ma'lumotlarni yig'ganda O'zbekiston
qonunchiligidagi shaxsiy ma'lumotlarni himoya qilish talablariga rioya qilish tavsiya etiladi —
foydalanuvchiga nima uchun ma'lumot so'ralayotgani aytilishi va ma'lumotlar xavfsiz saqlanishi
kerak.

## 6. Muhim eslatmalar

- **Telegram Stars real pul emas** — foydalanuvchi Stars sotib olganda, bu pul to'g'ridan-to'g'ri
  sizning hisobingizga (bot balance) tushadi, keyin uni Telegram orqali pul mablag'iga
  aylantirish (withdraw) mumkin. Rasmiy shartlar va komissiyalar bilan Telegram hujjatlaridan
  tanishing: https://core.telegram.org/bots/payments-stars
- **Premium sotish** uchun siz o'zingiz Fragment (fragment.com) yoki Telegram'ning rasmiy sovg'a
  funksiyasi orqali haqiqiy Premium'ni foydalanuvchiga yuborishingiz kerak — bot buni avtomatik
  qilmaydi, faqat buyurtma va to'lovni boshqaradi.
- Ushbu bot **buyurtma va to'lovlarni boshqarish tizimi**; haqiqiy Stars/Premium yetkazib
  berishni siz qo'lda yoki alohida integratsiya orqali amalga oshirishingiz kerak bo'ladi.

## 7. Serverga joylash (production)

### A) Oddiy usul — VPS + systemd (tavsiya etiladi)

```bash
# Serverda:
sudo mkdir -p /opt/stars_bot
cd /opt/stars_bot
# fayllarni shu papkaga yuklang, keyin:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && nano .env   # tokeningizni kiriting

# systemd xizmati sifatida o'rnatish:
sudo cp stars_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable stars_bot
sudo systemctl start stars_bot

# Holatini tekshirish:
sudo systemctl status stars_bot
journalctl -u stars_bot -f      # jonli loglarni ko'rish
```

Bu usulda bot server qayta yuklansa ham avtomatik ishga tushadi, yiqilib qolsa
(`Restart=on-failure`) o'zi qayta boshlanadi.

### B) Docker orqali

```bash
cp .env.example .env && nano .env
touch bot.db bot.log
docker compose up -d --build

# Loglarni ko'rish:
docker compose logs -f
```

### Muhim: bitta nusxada ishga tushiring

Bot **long polling** rejimida ishlaydi — shuning uchun bir vaqtning o'zida bitta joyda
(bitta server yoki bitta konteynerda) ishga tushirilishi kerak. Ikkita nusxa parallel ishlasa,
Telegram xatolik qaytaradi (`TelegramConflictError`).

### Zaxira nusxa (backup)

`bot.db` — barcha buyurtma va foydalanuvchi ma'lumotlari shu faylda. Uni muntazam
zaxiralab turing, masalan kunlik cron orqali:

```bash
0 3 * * * cp /opt/stars_bot/bot.db /opt/stars_bot/backups/bot_$(date +\%F).db
```

## 8. Loyiha tuzilishi

```
stars_bot/
├── bot.py                # botni ishga tushiruvchi asosiy fayl (log, xato ushlash bilan)
├── config.py              # sozlamalar va mahsulotlar katalogi
├── database.py             # SQLite bilan ishlash (aiosqlite, WAL rejimi, statistika)
├── keyboards.py            # inline va reply klaviaturalar
├── states.py               # FSM holatlari (chek kutish)
├── middlewares.py           # telefon raqamini majburiy qiluvchi middleware
├── handlers/
│   ├── start.py            # /start va asosiy menyu
│   ├── shop.py              # mahsulotlar katalogi
│   ├── payment.py           # Stars va karta to'lovlari
│   └── admin.py              # admin panel (buyurtmalar, statistika, broadcast, export)
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── stars_bot.service         # systemd namunasi
├── bot.db                    # SQLite ma'lumotlar bazasi (avtomatik yaratiladi)
└── bot.log                   # log fayli (avtomatik yaratiladi, 5MB dan oshsa aylanadi)
```

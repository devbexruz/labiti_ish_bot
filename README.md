<div align="center">

# 🤖 LABITI ISH BOT

**Google Sheets integratsiyali Telegram ish ariza boti**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.13-009688?logo=telegram&logoColor=white)](https://docs.aiogram.dev/)
[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-API-34A853?logo=googlesheets&logoColor=white)](https://developers.google.com/sheets/api)

</div>

---

## 📋 Loyiha haqida

**LABITI ISH BOT** — go'zallik sohasi (beauty industry) bo'yicha kadrlarni tanlash jarayonini avtomatlashtiradigan Telegram bot. Foydalanuvchilar botda kategoriya tanlab, anketa savollariga javob beradi va natijalar avtomatik ravishda Google Sheets jadvaliga yoziladi.

## ✨ Xususiyatlar

- 🌐 **Ko'p tilli qo'llab-quvvatlash** — O'zbek, Rus va Ingliz tillari
- 📂 **7 ta kasbiy kategoriya:**
  - Stilist · Kolorit · Vizajist · Manikyur/Pedikyur · Kiprikchi · Depilatsiya · Administrator
- ❓ **Turli xil savol formatlari** — matnli, variantli (inline-keyboard) va video
- 🎥 **Video qo'llab-quvvatlash** — foydalanuvchi video yuborsa, `file_id` yoki to'g'ridan-to'g'ri havola saqlanadi
- 📊 **Google Sheets integratsiya** — har bir kategoriya uchun alohida worksheet'ga avtomatik yozish
- ⬅️ **Ortga qaytish** — foydalanuvchi istalgan savoldan ortga qaytishi mumkin
- 🔔 **Admin panel** — `file_id` orqali videolarni ko'rish imkoniyati

## 🛠 Texnologiyalar

| Texnologiya | Versiya | Vazifasi |
|---|---|---|
| [Python](https://python.org) | 3.10+ | Asosiy dasturlash tili |
| [Aiogram](https://docs.aiogram.dev/) | 3.13.1 | Telegram Bot API framework |
| [gspread](https://docs.gspread.org/) | 6.1.2 | Google Sheets bilan ishlash |
| [google-auth](https://google-auth.readthedocs.io/) | 2.34.0 | Google autentifikatsiya |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | 1.0.1 | `.env` fayldan konfiguratsiya o'qish |

## 📁 Loyiha tuzilishi

```
labiti_ish_bot/
├── src/                    # Asosiy manba kodlar papkasi
│   ├── bot.py              # Asosiy bot fayli (handlerlar, FSM, ishga tushirish)
│   ├── questions.py        # Kategoriyalar va savollarni yuklash
│   ├── questions.json      # Savollar bazasi (JSON formatda)
│   ├── sheets_helper.py    # Google Sheets ga yozish funksiyalari
│   ├── translate.py        # Tarjima generatsiyasi uchun yordamchi skript
│   ├── utils.py            # Yordamchi funksiyalar (tarjima, callback parsing)
│   └── output.json         # Chiqish natijalarini saqlash
├── translate.json          # Tarjimalar lug'ati (UZ → RU, EN)
├── requirements.txt        # Python kutubxonalar ro'yxati
├── .env.example            # Muhit o'zgaruvchilari namunasi
├── .gitignore              # Git tomonidan e'tiborga olinmaydigan fayllar
└── README.md
```

## 🚀 O'rnatish va ishga tushirish

### Talablar

- Python 3.10 yoki undan yuqori
- Google Cloud Service Account (Sheets API yoqilgan)
- Telegram Bot Token ([BotFather](https://t.me/BotFather) orqali olinadi)

### 1. Repozitoriyani klonlash

```bash
git clone https://github.com/devbexruz/labiti_ish_bot.git
cd labiti_ish_bot
```

### 2. Virtual muhit yaratish (tavsiya etiladi)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Google Sheets sozlash

1. [Google Cloud Console](https://console.cloud.google.com/) da yangi loyiha yarating
2. **Google Sheets API** ni yoqing
3. **Service Account** yarating va JSON kalit faylini yuklab oling
4. Google Sheets jadvalingizni Service Account email'iga **Editor** huquqi bilan ulashing

### 5. Muhit o'zgaruvchilarini sozlash

Loyiha papkasida `.env` fayl yarating:

```env
BOT_TOKEN=your_telegram_bot_token
SPREADSHEET_URL=https://docs.google.com/spreadsheets/d/your_spreadsheet_id
GOOGLE_SERVICE_ACCOUNT_JSON=path/to/service-account.json
BOT_USERNAME=your_bot_username
ADMINS=admin_chat_id
```

| O'zgaruvchi | Tavsif |
|---|---|
| `BOT_TOKEN` | Telegram bot tokeni |
| `SPREADSHEET_URL` | Google Sheets jadval havolasi |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Service Account JSON kalit faylining yo'li |
| `BOT_USERNAME` | Bot username'i (`@` siz) |
| `ADMINS` | Admin foydalanuvchining chat ID raqami |

### 6. Botni ishga tushirish

```bash
python bot.py
```

## 📖 Foydalanish

1. Telegram'da botni oching va `/start` buyrug'ini yuboring
2. Tilni tanlang (O'zbek / Русский / English)
3. Kasbiy kategoriyani tanlang
4. Savollarga ketma-ket javob bering:
   - **Matnli savollar** — javobni yozing
   - **Variantli savollar** — tugmalardan birini bosing
   - **Video savollar** — video fayl yuboring
5. Barcha savollar tugagach, ariza Google Sheets'ga saqlanadi

## ⚠️ Eslatmalar

- Videolar Google Sheets'ga **yuklanmaydi**; faqat Telegram `file_id` yoki havola saqlanadi. Admin botga `Video:<file_id>` yuborib videoni ko'rishi mumkin.
- Har bir kategoriya uchun Google Sheets'da alohida **worksheet** avtomatik yaratiladi.
- Savollarni tahrirlash uchun `questions.json` faylini o'zgartiring.
- Tarjimalarni qo'shish/tahrirlash uchun `translate.json` faylidan foydalaning.

## 📄 Litsenziya

Ushbu loyiha shaxsiy foydalanish uchun mo'ljallangan.

---

<div align="center">

**LABITI** uchun yaratilgan ❤️

</div>

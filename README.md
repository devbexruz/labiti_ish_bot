# LABITI ISH BOT — Google Sheets integratsiya qilingan Telegram bot

Ushbu loyiha foydalanuvchi yuborgan TZ (kategoriya va savollar) asosida yaratilgan. Javoblar va video `file_id` lar Google Sheets ga yoziladi.

## Xususiyatlar
- Til tanlash (hozircha UZ).
- Kategoriya tanlash:
  - Stilist, Kolorit, Vizajist, Manikyur/Pedikyur, Kiprikchi, Depilatsiya, Administrator
- Har bir kategoriya uchun savollar ketma-ket ko‘rinishda.
- Variantli savollar uchun reply-keyboard.
- Video savollar uchun video qabul qilish va `file_id` ni saqlash.
- Natijalarni Google Sheets ga `append_row` orqali yozish (alohida kategoriya bo‘yicha worksheet).

## O‘rnatish
1) Python 3.10+ o‘rnating.
2) Kutubxonalarni o‘rnating:
```
pip install -r requirements.txt
```
3) Google Cloud Console:
   - Service Account yarating.
   - JSON kalitni yuklab oling.
   - `.env` faylda `GOOGLE_SERVICE_ACCOUNT_JSON` ga JSON yo‘lini kiriting.
   - Jadvalingizni service account email'iga **Share** qiling (Editor ruxsat).
4) `.env` fayl yarating (`.env.example` dan nusxa oling) va to‘ldiring.
5) Botni ishga tushiring:
```
python bot.py
```

## Eslatma
- Videolar Google Sheets’ga yuklanmaydi; faqat `file_id` saqlanadi. Kerak bo‘lsa admin botdan yuklab olishi mumkin.
- Google Drive’ga yuklash qo‘shilishi mumkin (qo‘shimcha API kerak).
- Aiogram v3 ishlatilgan.

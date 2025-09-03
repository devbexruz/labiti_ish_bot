import os
from typing import Dict, Any, List

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from questions import CATEGORIES, QUESTIONS
from sheets_helper import append_submission
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN .env da belgilanmagan")
if not SPREADSHEET_URL:
    raise RuntimeError("SPREADSHEET_URL .env da belgilanmagan")

bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- State machine ---
class ApplyForm(StatesGroup):
    language = State()
    category = State()
    q_index = State()

def lang_keyboard():
    kb = [[KeyboardButton(text="O‘zbek tili"), KeyboardButton(text="Русский (RU) — tez orada")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def categories_keyboard():
    rows = []
    row = []
    for i, cat in enumerate(CATEGORIES, start=1):
        row.append(KeyboardButton(text=cat))
        if i % 2 == 0:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text="🌐 Tilni tanlash")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, one_time_keyboard=True)

def choices_keyboard(options):
    rows = []
    row = []
    for i, opt in enumerate(options, start=1):
        row.append(KeyboardButton(text=opt))
        if i % 2 == 0:
            rows.append(row); row = []
    if row: rows.append(row)
    rows.append([KeyboardButton(text="⬅️ Ortga")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ApplyForm.language)
    await message.answer(
        "Assalomu alaykum!\nLABITI ish botiga xush kelibsiz.\nTilni tanlang:",
        reply_markup=lang_keyboard()
    )

@dp.message(ApplyForm.category, F.text == "🌐 Tilni tanlash")
async def back_from_category(message: Message, state: FSMContext):
    await state.set_state(ApplyForm.language)
    await message.answer("Tilni tanlang:", reply_markup=lang_keyboard())

@dp.message(ApplyForm.language)
async def choose_language(message: Message, state: FSMContext):
    # Hozircha faqat O'zbek
    await state.update_data(language="uz")
    await state.set_state(ApplyForm.category)
    await message.answer("Kategoriya tanlang:", reply_markup=categories_keyboard())

@dp.message(ApplyForm.category)
async def choose_category(message: Message, state: FSMContext):
    category = message.text.strip()
    if category not in QUESTIONS:
        await message.answer("Iltimos, menyudan kategoriya tanlang.", reply_markup=categories_keyboard())
        return
    await state.update_data(category=category, q_index=0, answers={}, videos={})
    q = QUESTIONS[category][0]
    kb = choices_keyboard(q["options"]) if q["type"] == "choice" else None
    await state.set_state(ApplyForm.q_index)
    await message.answer(q["text"], reply_markup=kb)

@dp.message(ApplyForm.q_index, F.text == "⬅️ Ortga")
async def back_from_questions(message: Message, state: FSMContext):
    data = await state.get_data()
    q_index = data.get("q_index", 0)
    if q_index == 0:
        await state.set_state(ApplyForm.category)
        await message.answer("Kategoriya tanlang:", reply_markup=categories_keyboard())
        return
    # move one step back
    await state.update_data(q_index=q_index-1)
    data = await state.get_data()
    category = data["category"]
    q = QUESTIONS[category][q_index-1]
    kb = choices_keyboard(q["options"]) if q["type"] == "choice" else None
    await message.answer(q["text"], reply_markup=kb)

@dp.message(ApplyForm.q_index, F.video | F.text)
async def collect_answers(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    q_index = data["q_index"]
    answers: Dict[str, Any] = data["answers"]
    videos: Dict[str, Any] = data["videos"]

    q = QUESTIONS[category][q_index]
    if q["type"] == "video":
        if message.video:
            file_info = await bot.get_file(message.video.file_id)
            file_path = file_info.file_path
            file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            videos[q["text"]] = file_url
        else:
            await message.answer("Iltimos, video yuboring yoki '⬅️ Ortga' tugmasidan foydalaning.", reply_markup=choices_keyboard([]))
            return
    elif q["type"] == "choice":
        # Matn variantlardan biri bo'lishi shart
        opt = (message.text or "").strip()
        if opt not in q["options"]:
            await message.answer("Iltimos, variantlardan birini tanlang.", reply_markup=choices_keyboard(q["options"]))
            return
        answers[q["text"]] = opt
    else:
        answers[q["text"]] = (message.text or "").strip()

    q_index += 1
    if q_index >= len(QUESTIONS[category]):
        # Save to Google Sheets
        answers.update(videos)
        print(answers, category)
        try:
            await message.answer(
                "Biroz kuting ...",
                reply_markup=categories_keyboard()
            )
            append_submission(
                spreadsheet_url=SPREADSHEET_URL,
                sheet_name=category,
                answers=answers
            )
            await message.answer(
                "✅ Arizangiz muvaffaqiyatli yuborildi!\nRahmat! Ma’lumotlaringiz qabul qilindi va tizimga saqlandi.\nTez orada administrator siz bilan bog‘lanadi.\n\n📞 Savollar bo‘lsa, shu yerda yozishingiz mumkin."
            )
        except Exception as e:
            print(str(e))
            await message.answer(
                "❌ Saqlashda xatolik yuz berdi. Qayta urunib ko'ring yoki administratorga murojaat qiling.",
                reply_markup=categories_keyboard()
            )
        await state.clear()
        return

    # Ask next question
    await state.update_data(q_index=q_index, answers=answers, videos=videos)
    next_q = QUESTIONS[category][q_index]
    kb = choices_keyboard(next_q["options"]) if next_q["type"] == "choice" else choices_keyboard([])
    await message.answer(next_q["text"], reply_markup=kb)

if __name__ == "__main__":
    import asyncio
    async def main():
        print("Bot ishga tushmoqda...")
        await dp.start_polling(bot)
    asyncio.run(main())

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
from utils import to_translate
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")
BOT_USERNAME = os.getenv("BOT_USERNAME")

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
    kb = [[KeyboardButton(text="O‘zbek tili"), KeyboardButton(text="Русский"), KeyboardButton(text="English")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def categories_keyboard(lang):
    rows = []
    row = []
    for i, cat in enumerate(CATEGORIES, start=1):
        row.append(KeyboardButton(text=to_translate(lang, cat)))
        if i % 2 == 0:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text=to_translate(lang, "🌐 Tilni tanlash"))])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, one_time_keyboard=True)

def choices_keyboard(options, lang):
    rows = []
    row = []
    for i, opt in enumerate(options, start=1):
        row.append(KeyboardButton(text=to_translate(lang, opt)))
        if i % 2 == 0:
            rows.append(row); row = []
    if row: rows.append(row)
    rows.append([KeyboardButton(text=to_translate(lang, "⬅️ Ortga"))])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ApplyForm.language)
    await message.answer(
        """Uz: Assalomu alaykum!
LABITI ish botiga xush kelibsiz.

En: Hello!
Welcome to the LABITI job bot.

Ru: Здравствуйте!
Добро пожаловать в бот вакансий LABITI.

Tilni tanlang (Please select a language, Выберите язык):
""",
        reply_markup=lang_keyboard()
    )

@dp.message(ApplyForm.category, F.text.in_([
    "🌐 Tilni tanlash",
    to_translate("ru", "🌐 Tilni tanlash"),
    to_translate("en", "🌐 Tilni tanlash")
]))
async def back_from_category(message: Message, state: FSMContext):
    await state.set_state(ApplyForm.language)
    await message.answer("Tilni tanlang:", reply_markup=lang_keyboard())

@dp.message(ApplyForm.language)
async def choose_language(message: Message, state: FSMContext):
    # Hozircha faqat O'zbek
    if message.text == "O‘zbek tili":
        await state.update_data(language="uz")
    elif message.text == "Русский":
        await state.update_data(language="ru")
    elif message.text == "English":
        await state.update_data(language="en")
    else:
        await message.answer("Bunday til mavjud emas\nIltimos menyudan biror tilni tanlang!", reply_markup=lang_keyboard())
        return

    await state.set_state(ApplyForm.category)
    data = await state.get_data()
    language = data["language"]
    await message.answer(to_translate(language, "Kategoriyani tanlang:"), reply_markup=categories_keyboard(language))

@dp.message(ApplyForm.category)
async def choose_category(message: Message, state: FSMContext):
    data = await state.get_data()
    language = data["language"]
    text = message.text.strip()
    current_category = ""
    for category in QUESTIONS:
        if to_translate(language, category) == text:
            current_category = category
            break
    if current_category == "":
        await message.answer(to_translate(language, "Iltimos, menyudan kategoriya tanlang."), reply_markup=categories_keyboard(language))
        return
    await state.update_data(category=current_category, q_index=0, answers={}, videos={})
    q = QUESTIONS[current_category][0]
    kb = choices_keyboard(q["options"], language) if q["type"] == "choice" else choices_keyboard([], language)
    await state.set_state(ApplyForm.q_index)
    await message.answer(to_translate(language, q["text"]), reply_markup=kb)

@dp.message(ApplyForm.q_index, F.text.in_(["⬅️ Ortga", to_translate("ru", "⬅️ Ortga"), to_translate("en", "⬅️ Ortga")]))
async def back_from_questions(message: Message, state: FSMContext):
    data = await state.get_data()
    language = data["language"]
    print(language)
    data = await state.get_data()
    q_index = data.get("q_index", 0)
    if q_index == 0:
        await state.set_state(ApplyForm.category)
        await message.answer(to_translate(language, "Kategoriyani tanlang:"), reply_markup=categories_keyboard(language))
        return
    # move one step back
    await state.update_data(q_index=q_index-1)
    data = await state.get_data()
    category = data["category"]
    q = QUESTIONS[category][q_index-1]
    kb = choices_keyboard(q["options"], language) if q["type"] == "choice" else choices_keyboard([], language)
    await message.answer(to_translate(language, q["text"]), reply_markup=kb)

@dp.message(ApplyForm.q_index, F.video | F.text)
async def collect_answers(message: Message, state: FSMContext):
    data = await state.get_data()
    language = data["language"]
    data = await state.get_data()
    category = data["category"]
    q_index = data["q_index"]
    answers: Dict[str, Any] = data["answers"]
    videos: Dict[str, Any] = data["videos"]

    q = QUESTIONS[category][q_index]
    if q["type"] == "video":
        if message.video:
            try:
                file_info = await bot.get_file(message.video.file_id)
                file_path = file_info.file_path
                file_url = f"=HYPERLINK(\"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}\";\"Video\")"
                videos[q["text"]] = file_url
            except:
                videos[q["text"]] =  f"=HYPERLINK(\"https://t.me/{BOT_USERNAME[1:]}?start={message.video.file_id}\";\"Katta Video\")"
        else:
            await message.answer(to_translate(language, "Iltimos, video yuboring yoki '⬅️ Ortga' tugmasidan foydalaning."), reply_markup=choices_keyboard([], language))
            return
    elif q["type"] == "choice":
        # Matn variantlardan biri bo'lishi shart
        opt = (message.text or "").strip()
        answers[q["text"]] = False
        for o in q["options"]:
            if opt == to_translate(language, o):
                answers[q["text"]] = opt
                break
        if answers[q["text"]] == False:
            await message.answer(to_translate(language, "Iltimos, variantlardan birini tanlang."), reply_markup=choices_keyboard(q["options"], language))
            return
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
                reply_markup=categories_keyboard(language)
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
                reply_markup=categories_keyboard(language)
            )
        await state.clear()
        return

    # Ask next question
    await state.update_data(q_index=q_index, answers=answers, videos=videos)
    next_q = QUESTIONS[category][q_index]
    kb = choices_keyboard(next_q["options"], language) if next_q["type"] == "choice" else choices_keyboard([], language)
    await message.answer(to_translate(language, next_q["text"]), reply_markup=kb)

if __name__ == "__main__":
    import asyncio
    async def main():
        print("Bot ishga tushmoqda...")
        await dp.start_polling(bot)
    asyncio.run(main())

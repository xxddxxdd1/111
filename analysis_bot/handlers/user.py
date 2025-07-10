from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command, CommandObject

from database import find_analysis_by_name

router = Router()

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Найти анализ")],
        [KeyboardButton(text="📂 Категории анализов")],
    ],
    resize_keyboard=True
)

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "👋 Привет! Я — бот-справочник по лабораторным анализам.\n"
        "🔍 Используй кнопку «Найти анализ» или напиши его название.",
        reply_markup=main_menu
    )

@router.message()
async def handle_text(message: Message):
    text = message.text.strip().lower()

    if text == "🔍 найти анализ":
        await message.answer("🔍 Введите название анализа.")
        return

    if text == "📂 категории анализов":
        await message.answer("📂 Здесь будут категории (ещё не реализовано).")
        return

    result = find_analysis_by_name(text)
    if result:
        name, category, units, norms, description = result
        await message.answer(
            f"<b>📋 Название:</b> {name}\n"
            f"<b>🧪 Категория:</b> {category}\n"
            f"<b>📏 Единицы:</b> {units}\n"
            f"<b>📊 Нормы:</b> {norms}\n"
            f"<b>ℹ️ Описание:</b> {description}",
            parse_mode="HTML"
        )
    else:
        await message.answer("❌ Анализ не найден. Попробуйте уточнить название.")

@router.message(Command("анализ"))
async def handle_cmd_analysis(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("❗ Укажите ключевое слово. Пример: /анализ глюкоза")
        return

    keyword = command.args.strip()
    result = find_analysis_by_name(keyword)

    if result:
        name, category, units, norms, description = result
        await message.answer(
            f"<b>📋 Название:</b> {name}\n"
            f"<b>🧪 Категория:</b> {category}\n"
            f"<b>📏 Единицы:</b> {units}\n"
            f"<b>📊 Нормы:</b> {norms}\n"
            f"<b>ℹ️ Описание:</b> {description}",
            parse_mode="HTML"
        )
    else:
        await message.answer("❌ Анализ не найден. Попробуйте уточнить.")

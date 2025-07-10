from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from myconfig import ADMINS
from database import add_analysis, list_analyses, delete_analysis

router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in ADMINS

@router.message(Command("add"))
async def cmd_add(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав.")
        return

    text = message.text.partition("\n")[2]
    if not text:
        await message.answer("Формат:\n"
                             "/add\n"
                             "Название: ...\nКатегория: ...\nЕдиницы: ...\nНормы: ...\nОписание: ...")
        return

    lines = [line.strip() for line in text.split("\n") if ":" in line]
    data = {}
    for line in lines:
        key, _, value = line.partition(":")
        data[key.lower()] = value.strip()

    required = ["название", "категория", "единицы", "нормы", "описание"]
    if not all(k in data for k in required):
        await message.answer("❗ Не все поля заполнены.")
        return

    try:
        add_analysis(
            data["название"],
            data["категория"],
            data["единицы"],
            data["нормы"],
            data["описание"]
        )
        await message.answer("✅ Анализ добавлен.")
    except Exception as e:
        await message.answer(f"❌ Ошибка при добавлении: {e}")

# =============== Список анализов с пагинацией ===============

PAGE_SIZE = 5

@router.message(Command("list_admin"))
async def cmd_list_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав.")
        return
    await send_admin_list(message, page=0)

@router.callback_query(F.data.startswith("admin_list_page:"))
async def paginate(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет прав", show_alert=True)
        return
    page = int(callback.data.split(":")[1])
    await send_admin_list(callback, page)

@router.callback_query(F.data.startswith("del:"))
async def handle_delete(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет прав", show_alert=True)
        return

    analysis_id = int(callback.data.split(":")[1])
    delete_analysis(analysis_id)
    await callback.answer("❌ Удалено", show_alert=True)
    await send_admin_list(callback, page=0)

async def send_admin_list(target, page: int = 0):
    offset = page * PAGE_SIZE
    records = list_analyses(offset=offset, limit=PAGE_SIZE)

    if not records:
        await target.answer("Список пуст.")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"❌ Удалить {name}", callback_data=f"del:{_id}")]
        for _id, name in records
    ])
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"admin_list_page:{page-1}"))
    if len(records) == PAGE_SIZE:
        nav_buttons.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"admin_list_page:{page+1}"))
    if nav_buttons:
        kb.inline_keyboard.append(nav_buttons)

    text = "🗂️ Список анализов:"
    if hasattr(target, "message"):
        await target.message.edit_text(text, reply_markup=kb)
    else:
        await target.answer(text, reply_markup=kb)

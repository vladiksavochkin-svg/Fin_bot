from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup
import app.database.requestes as req
async def get_income_category_kb():
    kb=ReplyKeyboardBuilder()#пустой список кнопок
    categories=await req.get_income_categories()
    for c in categories:
        btn=KeyboardButton(text=c.name)
        kb.add(btn)
    kb.adjust(2)#по 2 кнопки в 1 ряд
    return kb.as_markup()#превращение из списка в клавиатуру
async def get_expense_category_kb():
    kb=ReplyKeyboardBuilder()#пустой список кнопок
    categories=await req.get_expence_categories()
    for c in categories:
        btn=KeyboardButton(text=c.name)
        kb.add(btn)
    kb.adjust(2)#по 2 кнопки в 1 ряд
    return kb.as_markup()#превращение из списка в клавиатуру
starts_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Доход"), KeyboardButton(text="💸 Расход")],
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="📈 История")]
    ],
    resize_keyboard=True
)
skip_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Пропустить')]])
category_types_kb=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='доход')], [KeyboardButton(text='расход')]])
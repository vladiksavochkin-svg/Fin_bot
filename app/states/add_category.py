from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.database.requestes import get_income_categories, get_expence_categories


def get_income_kb():
    kb=ReplyKeyboardBuilder()#пустой список кнопок
    categories= get_income_categories()
    for c in categories:
        b=KeyboardButton(text=f'{c[0]} {c[1]}')
        kb.add(b)
    kb.adjust(2)#по 2 кнопки в 1 ряд
    return kb.as_markup(resize_keyboard=True)


def get_expence_kb():
    kb=ReplyKeyboardBuilder()#пустой список кнопок
    categories= get_expence_categories()
    for c in categories:
        b=KeyboardButton(text=f'{c[0]} {c[1]}')
        kb.add(b)
    kb.adjust(2)#по 2 кнопки в 1 ряд
    return kb.as_markup(resize_keyboard=True)

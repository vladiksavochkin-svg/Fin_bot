from aiogram import F,Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.keyboards.user_keyboards import skip_kb
from app.keyboards.user_keyboards import get_income_category_kb
from aiogram.types import Message
from app.database.requestes import add_transaction
from app.keyboards.user_keyboards import starts_kb
from aiogram.filters import Command,or_f
router2=Router()

class Income(StatesGroup):
    summa=State()
    category=State()
    description=State()

@router2.message(or_f(F.text=='💰 Доход',Command('income')))
async def income_handler(message:Message,state:FSMContext):
    await state.set_state(Income.summa)
    await message.answer('Введите сумму дохода:')


@router2.message(Income.summa)
async def income_summa(message:Message,state:FSMContext):
    await state.update_data(summa=message.text)
    await state.set_state(Income.category)
    await message.answer('Выбери категорию или напиши свою:',reply_markup=await get_income_category_kb())


@router2.message(Income.category)
async def income_category(message:Message,state:FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(Income.description)
    await message.answer('Добавь описание или пропусти:',reply_markup=skip_kb)


@router2.message(Income.description)
async def income_description_handler(message:Message,state:FSMContext):
    if message.text!='Пропустить':
        await state.update_data(description=message.text)
    else:
       await state.update_data(description=None)
    data=await state.get_data()
    await state.clear()
    await add_transaction(message.from_user.id,data['category'],int(data['summa']),data['description'])
    await message.answer(f'''Доход добавлен✅
    Сумма:{data['summa']}₽
    Категория:{data['category']}
    Описание:{data['description']}''',reply_markup=starts_kb)

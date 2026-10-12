from aiogram import F,Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from app.keyboards.user_keyboards import skip_kb
from app.keyboards.user_keyboards import starts_kb
from app.keyboards.user_keyboards import get_expense_category_kb
from app.database.requestes import add_transaction
from aiogram.filters import Command,or_f
class Expenditure(StatesGroup):
    summa=State()
    category=State()
    description=State()

router1=Router()

@router1.message(or_f(F.text=='💸 Расход',Command('expence')))
async def expense_handler(message:Message,state:FSMContext):
    await state.set_state(Expenditure.summa)
    await message.answer('Введите сумму расхода:')


@router1.message(Expenditure.summa)
async def expence_summa(message:Message,state:FSMContext):
    await state.update_data(summa=message.text)
    await state.set_state(Expenditure.category)
    await message.answer('Выбери категорию или напиши свою:',reply_markup=await get_expense_category_kb())


@router1.message(Expenditure.category)
async def expence_category(message:Message,state:FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(Expenditure.description)
    await message.answer('Добавь описание или пропусти:',reply_markup=skip_kb)


@router1.message(Expenditure.description)
async def expence_category_handler(message:Message,state:FSMContext):
    if message.text!='Пропустить':
        await state.update_data(description=message.text)
    else:
       await state.update_data(description=None)
    data=await state.get_data()
    await state.clear()
    await add_transaction(message.from_user.id,data['category'],int(data['summa']),data['description'])
    await message.answer(f'''Расход добавлен✅
    Сумма:{data['summa']}₽
    Категория:{data['category']}
    Описание:{data['description']}''',reply_markup=starts_kb)

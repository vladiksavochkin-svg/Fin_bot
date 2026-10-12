from aiogram import Router

from app.database.requestes import add_new_category
from app.filteres.admin import IsAdmin
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states.add_category_states import AddCategoryStates
from app.keyboards.user_keyboards import category_types_kb
admin_router = Router()
incomes=['выплата','продажа','зарплата','подарок','фриланс']
@admin_router.message(IsAdmin(),Command('add_category'))
async def add_category_kmd(message: Message, state: FSMContext):
    await state.set_state(AddCategoryStates.name)
    await message.answer('Введите имя новой категории')
@admin_router.message(AddCategoryStates.name)
async def add_category_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddCategoryStates.type)
    await message.answer('Укажите тип новой категории',reply_markup=category_types_kb)
@admin_router.message(AddCategoryStates.type)
async def add_category_type(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    data=await state.get_data()
    await state.clear()
    await add_new_category(data['name'],data['type'])
    await message.answer(f'''Категория добавлена!
Название:{data['name']}
Тип:{data['type']}''')
    if data['type']=='доход':
        incomes.append(data['name'])
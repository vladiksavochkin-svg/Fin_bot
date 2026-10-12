from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from .admin_handlers import incomes

from app.database.requestes import get_all_transactions,get_category_by_id
from app.keyboards.user_keyboards import starts_kb
user_router = Router()

@user_router.message(Command('start'))
async def start(message:Message):
    await message.answer(f'''👋 Привет,{message.from_user.first_name}!

    Я бот для отслеживания твоих трат и заработков

    Выбери действие:''',reply_markup=starts_kb)


@user_router.message(F.text=='📈 История')
async def history(message:Message):
    id=message.from_user.id
    operations=await get_all_transactions(id)
    print(operations)
    text='''📈ПОСЛЕДНИЕ ТРАНЗАКЦИИ:'''
    for transaction in operations:
        category=await get_category_by_id(transaction.category_id)
        if category.type=='доход':
            text+=(f'''
💰{transaction.date}
+{transaction.amount}₽|{category.name}''')
        else:
            text+=f'''
💸{transaction.date}
-{transaction.amount}₽|{category.name}'''
    await message.answer(text)


@user_router.message(F.text=='📊 Статистика')
async def statistic(message:Message):
    id=message.from_user.id
    o=await get_all_transactions(id)
    income=0
    expendeture=0
    categories={}
    for i in o:
        category=await get_category_by_id(i.category_id)
        if category.type=='доход':
            income+=int(i.amount)
        else:
            expendeture+=int(i.amount)
        if o[3] not in categories:
            categories[category.name]=int(i.amount)
        else:
            categories[category.name]+=int(i.amount)
    text2=f'''ПОДРОБНАЯ СТАТИСТИКА

Всего доход:{income}
Всего расходы:{expendeture}
Итоговый баланс:{income-expendeture}

Расходы по категориям:

    '''
    for a,i in categories.items():
        if a not in incomes and expendeture!=0:
            text2+=f'{a} : {i}₽ ({int(i*100/expendeture)}%)  \n'
    text2+='Доходы по категориям:   \n'
    for a,i in categories.items():
        if a in incomes and income!=0:
            text2+=f'{a} : {i}₽ ({int(i*100/income)}%)\n'
    await message.answer(text2)
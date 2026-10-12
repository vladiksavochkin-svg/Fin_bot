from sqlalchemy import select
from .models import async_session,Category,Transaction

async def get_income_categories():
    #создаём сессию-подключаемся к бд
    async with async_session() as session:
        #scalars-много,scalar-1,select-выбирать,where-фильтр
        categories=await session.scalars(select(Category).where(Category.type=='доход'))
        return categories
async def get_expence_categories():
    #создаём сессию-подключаемся к бд
    async with async_session() as session:
        #scalars-много,scalar-1,select-выбирать,where-фильтр
        categories=await session.scalars(select(Category).where(Category.type=='расход'))
        return categories

async def add_transaction(user_id,category_name,amount,comment):
    async with async_session() as session:
        category=await session.scalar(select(Category).where(Category.name==category_name))
        new_transaction=Transaction(user_id=user_id, amount=amount,
                                    comment=comment, category_id=category.id)
        #добавление в сессию
        session.add(new_transaction)
        #сохранение изменений в бд
        await session.commit()

async def get_all_transactions(id):
    async with async_session() as session:
        history=await session.scalars(select(Transaction).where(Transaction.user_id == id))
        return list(history)

async def get_category_by_id(category_id):
    async with async_session() as session:
        return await session.get(Category,category_id)

async def add_new_category(name,type):
    async with async_session() as session:
        new_category=Category(name=name,type=type)
        session.add(new_category)
        await session.commit()

async def get_total_by_type(user_id,category_type):
    async with async_session() as session:
        category_ides=await session.scalars(select(Category.id).where(Category.type==category_type))
        all_transactions=await session.scalars(select(Transaction.amount).where(Transaction.category_id.in_(category_ides),Transaction.user_id == user_id))
        return sum(list(all_transactions))

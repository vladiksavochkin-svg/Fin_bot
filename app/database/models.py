from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
from sqlalchemy import Integer,String,DateTime,ForeignKey
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
engine=create_async_engine(os.getenv('SQLALCHEMY_URL'))# движок для подключения к бд
async_session =async_sessionmaker(engine)# переменная для создания сессий

class Base(AsyncAttrs, DeclarativeBase):
    # класы чтобы другие классы создавать с него и объединять
    pass
class Category(Base):
    __tablename__='categories'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String)
    type:Mapped[str]=mapped_column(String)
class Transaction(Base):
    __tablename__='transactions'
    id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
    #primary key-столбец благодаря которому каждая строка уникальна
    #autoincrement-генерация автомотическая(нам не нужно ничего заполнять)
    user_id:Mapped[int]=mapped_column(Integer)
    category_id=mapped_column(ForeignKey('categories.id'))
    amount:Mapped[int]=mapped_column(Integer)
    comment:Mapped[str]=mapped_column(String,nullable=True)
    date:Mapped[datetime]=mapped_column(DateTime,default=datetime.now)

#создание таблиц из классов
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
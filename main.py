import asyncio
from aiogram import Bot, Dispatcher
from app.handlers.user_handlers import user_router
from app.states.add_expence import router1
from app.states.add_income import router2
from app.database.models import create_tables
from app.handlers.admin_handlers import admin_router
from dotenv import load_dotenv
import os
load_dotenv()
bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()


#основная функция
async def main():
    """Запуск бота"""
    print("Бот запущен")
    await create_tables()
    try:
        dp.include_routers(user_router,router2,router1,admin_router)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
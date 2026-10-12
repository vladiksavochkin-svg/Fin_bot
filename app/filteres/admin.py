from aiogram.filters import BaseFilter
from aiogram.types import Message

ADMIN_IDES=[7874283243]
class IsAdmin(BaseFilter):
    #метод срабатывается если в коде вызывается этот класс IsAdmin()
    async def __call__(self, message: Message):
        return message.from_user.id in ADMIN_IDES
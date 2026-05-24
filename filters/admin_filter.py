from aiogram.filters import BaseFilter
from aiogram.types import Message

from constants import ADMIN_ID


class AdminFilter(BaseFilter):

    async def __call__(self, message: Message):

        return message.from_user.id == ADMIN_ID
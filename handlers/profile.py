from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.db import (
    is_premium
)

router = Router()


@router.message(Command("profile"))
async def profile(message: Message):

    premium = is_premium(
        message.from_user.id
    )

    status = (
        "⭐ PREMIUM"
        if premium
        else "🆓 FREE"
    )

    await message.answer(
        f"👤 PROFILE\n\n"
        f"Status: {status}"
    )
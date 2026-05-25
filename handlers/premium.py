from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("premium"))
async def premium(message: Message):

    text = (
        "⭐ PREMIUM\n\n"

        "✅ Unlimited downloads\n"
        "✅ Faster speed\n"
        "✅ HQ audio\n"
        "✅ No ads\n"
        "✅ AI features\n\n"

        "💳 Price: 5$/month"
    )

    await message.answer(text)
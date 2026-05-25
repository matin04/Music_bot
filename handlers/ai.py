from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from services.ai_service import ask_ai

router = Router()


@router.message(Command("ai"))
async def ai_chat(message: Message):

    text = message.text.replace(
        "/ai",
        ""
    ).strip()

    if not text:

        await message.answer(
            "❌ Савол навис"
        )

        return

    await message.answer(
        "🤖 AI фикр карда истодааст..."
    )

    answer = ask_ai(text)

    await message.answer(answer)
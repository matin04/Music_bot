from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from services.recommendation_ai import (
    recommend_music
)

router = Router()


@router.message(Command("recommend"))
async def recommend(message: Message):

    query = message.text.replace(
        "/recommend",
        ""
    ).strip()

    if not query:

        await message.answer(
            "❌ Суруд навис"
        )

        return

    await message.answer(
        "🎵 AI recommendation..."
    )

    result = recommend_music(query)

    await message.answer(result)
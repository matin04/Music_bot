from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject

from utils.rate_limiter import RateLimiter


rate_limiter = RateLimiter(4)


class RateLimitMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable,
        event: TelegramObject,
        data: Dict[str, Any]
    ):

        user = data.get("event_from_user")

        if user:

            allowed = rate_limiter.is_allowed(
                user.id
            )

            if not allowed:

                if hasattr(event, "answer"):
                    await event.answer(
                        "⏳ Лутфан интизор шавед..."
                    )

                return

        return await handler(event, data)
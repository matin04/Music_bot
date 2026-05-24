from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable

from aiogram.types import TelegramObject

from utils.logger import logger


class LoggingMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[
            [TelegramObject, Dict[str, Any]],
            Awaitable[Any]
        ],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        user = data.get("event_from_user")

        if user:
            logger.info(
                f"User {user.id} triggered event"
            )

        return await handler(event, data)
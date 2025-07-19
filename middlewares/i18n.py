from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from keyboards import select_language
from redis.asyncio import Redis
from lexicon import LEXICON_RU, LEXICON_EN


class LexiconMiddleware(BaseMiddleware):
    """Мидлварь для правильной работы мультиязычности"""

    def __init__(self, redis: Redis):
        self.redis = redis

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        lang = await self.redis.get(f"user:{user_id}:lang")
        lang = lang.decode() if lang else None
        if lang not in ("RU", "EN"):
            # Не выбран язык? Значит даём пользователю клавиатуру и ждём от сервера следующего апдейта.
            if isinstance(event, Message):
                await event.answer(
                    "Choose your language / Выберите язык:",
                    reply_markup=select_language(),
                )
            return await handler(event, data)

        else:
            # Заносим в словарь data словарь с языком, который выбрал пользователь и нативно даём всем хендлерам как аргумент lexicon
            lexicon = LEXICON_RU if lang == "RU" else LEXICON_EN
            data["lexicon"] = lexicon
        return await handler(event, data)

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from typing import Any, Callable, Dict, Awaitable
from collections import defaultdict
from config import Config, load_config
from redis.asyncio import Redis
import time
import asyncio
from asyncio import Lock


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis):
        self.last_time = defaultdict(float)
        self.redis = redis
        self.lock = Lock()  # Защита от race condition

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Получаем объект пользователя
        user_id = event.from_user.id
        user = data.get("event_from_user", None)
        spam = await self.redis.get(f"user:{user_id}:spam")
        spam = int(spam.decode()) if spam else 0
        # Пропускаем события без пользователя
        if user is None:
            return await handler(event, data)
        if not isinstance(event, Message):
            return await handler(event, data)
        user_id = user.id
        current_time = time.monotonic()
        elapsed = current_time - self.last_time[user_id]
        if spam == 1:
            if elapsed >= 10:
                await self.redis.set(f"user:{user_id}:spam", 0)
                return await handler(event, data)
            else:
                return

        # Получаем лимит из config
        config: Config = load_config()
        rate_limit = float(config.bot.rate_lim)

        if 0 < rate_limit <= elapsed:
            self.last_time[user_id] = current_time
        if 0 < elapsed < rate_limit:
            delay = rate_limit - elapsed
            lexicon = data["lexicon"]
            await self.redis.set(f"user:{user.id}:spam", 1)
            await asyncio.sleep(
                delay
            )  # Необходимая задержка, не перегружаем сервера Телеграма.
            return await event.answer(lexicon["throttling"])

        return await handler(event, data)

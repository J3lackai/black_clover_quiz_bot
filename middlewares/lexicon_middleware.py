from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from lexicon import LEXICON_RU, LEXICON_EN
from keyboards import select_language
from redis.asyncio import Redis
from aiogram.fsm.context import FSMContext
from states.states import FSMFillForm as f


class LexiconMiddleware(BaseMiddleware):
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
        state: FSMContext = data.get("state")
        cur_state = await state.get_state()
        if lang not in ("RU", "EN") or cur_state == f.settings:
            if isinstance(event, Message):
                # язык ещё не выбран — отправляем клавиатуру выбора и не продолжаем цепочку
                await state.set_state(cur_state)
                await event.answer(
                    "Choose your language / Выберите язык:",
                    reply_markup=select_language(),
                )
            return await handler(event, data)

        # подставляем словарь в зависимости от языка
        data["lexicon"] = LEXICON_RU if lang == "RU" else LEXICON_EN
        return await handler(event, data)

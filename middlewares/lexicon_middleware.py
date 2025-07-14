from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from lexicon import LEXICON_RU, LEXICON_EN
from keyboards import select_language
from aiogram.types import TelegramObject


class LexiconMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        state = data.get("state")

        if not state:
            print("here")
            data["lexicon"] = LEXICON_RU
            result = await handler(event, data)
            return result

        user_data = await state.get_data()
        lexicon = user_data.get("lexicon")

        # Если язык ещё не выбран
        if lexicon not in ("RU", "EN"):
            if isinstance(event, Message):
                await event.answer(
                    "Choose your language / Выберите язык:",
                    reply_markup=select_language(),
                )
            # Здесь вызываем хендлер выбора языка, чтобы всё дошло до его выбора в process_language_choice
            result = await handler(event, data)
            return result

        # Устанавливаем словарь языка
        lexicon = LEXICON_RU if lexicon == "RU" else LEXICON_EN
        data["lexicon"] = lexicon
        result = await handler(event, data)
        return result

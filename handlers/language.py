from aiogram import Router, F
from aiogram.types import Message
from loguru import logger
from aiogram.filters import StateFilter
from redis.asyncio import Redis
from states.states import FSMFillForm as f
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(F.text.in_({"RU", "EN"}), StateFilter(f.settings))
async def process_language_choice(message: Message, redis: Redis, state: FSMContext):
    lang = message.text

    await redis.set(f"user:{message.from_user.id}:lang", lang)
    await state.clear()
    logger.info(f"Language set to {lang} for user {message.from_user.id}")

    if lang == "RU":
        await message.answer("Язык установлен на Русский")
    else:
        await message.answer("Language set to English")

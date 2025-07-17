from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from loguru import logger
from aiogram.filters import StateFilter, or_f
from redis.asyncio import Redis
from aiogram.fsm.state import default_state
from keyboards import select_language
from handlers.user import process_start_command
from lexicon import LEXICON_EN, LEXICON_RU

router = Router()


@router.message(or_f(F.text == "RU", F.text == "EN"), StateFilter(default_state))
async def process_language_choice(message: Message, redis: Redis):
    lang = message.text

    await redis.set(f"user:{message.from_user.id}:lang", lang)
    logger.info(f"Язык установлен на {lang} для пользователя: {message.from_user.id}")

    if lang == "RU":
        await message.answer(
            "Язык установлен на Русский", reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Language set to English", reply_markup=ReplyKeyboardRemove()
        )
    lexicon = LEXICON_RU if lang == "RU" else LEXICON_EN
    await process_start_command(message, redis, lexicon)


@router.message(
    or_f(F.text == "Выбрать язык", F.text == "Select a language"),
    StateFilter(default_state),
)
async def language_handler(message: Message):
    await message.answer(
        "Выберите язык / Choose your language:",
        reply_markup=select_language(),
    )

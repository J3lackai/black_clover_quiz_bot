from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loguru import logger

router = Router()


@router.message(F.text.in_({"RU", "EN"}))
async def process_language_choice(message: Message, state: FSMContext):
    lexicon = message.text.upper()
    await state.update_data(lexicon=lexicon)
    logger.info(f"Language set to {lexicon} for user {message.from_user.id}")

    if lexicon == "RU":
        await message.answer("Язык установлен на Русский")
    else:
        await message.answer("Language set to English")

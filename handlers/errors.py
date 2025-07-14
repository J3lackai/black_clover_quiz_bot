# Этот хэндлер срабатывает на неизвестные команды
from aiogram.types import Message
from aiogram import Router
from lexicon import LEXICON_EN, LEXICON_RU
from aiogram.fsm.context import FSMContext

router = Router()


@router.message()
async def process_unvalid_commands(message: Message, state: FSMContext):
    data = await state.get_data()
    lexicon = LEXICON_RU if data.get("lexicon", "RU") == "RU" else LEXICON_EN
    await message.answer(text=lexicon["unvalid"])

# Этот хэндлер срабатывает на неизвестные команды
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext

router = Router()


@router.message()
async def process_unvalid_commands(
    message: Message, state: FSMContext, lexicon: dict[str:str]
):
    await message.answer(text=lexicon["unvalid"])
    await state.clear()

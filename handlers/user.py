from aiogram import Router, F
from keyboards import main_menu
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from lexicon import LEXICON_RU

from aiogram.fsm.state import default_state


# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU["/start"], reply_markup=main_menu)


@router.message(
    or_f(Command("donate"), F.text.casefold() == "Поддержать автора"),
    StateFilter(default_state),
)
async def donate_handler(message: Message):
    await message.answer(LEXICON_RU["/donate"])


# Этот хэндлер срабатывает на команду /help
@router.message(
    or_f(Command("help"), F.text.casefold() == "Помощь"), StateFilter(default_state)
)
async def help_handler(message: Message):
    await message.answer(LEXICON_RU["/help"], reply_markup=main_menu)

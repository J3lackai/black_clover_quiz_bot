from aiogram import Router, F
from keyboards import get_main_menu
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from loguru import logger
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from lexicon import LEXICON_EN, LEXICON_RU

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    logger.debug("Пользователь отправил команду /start")
    data = await state.get_data()
    lang = data.get("lexicon", "RU")
    lexicon = LEXICON_RU if lang == "RU" else LEXICON_EN
    await message.answer(
        text=lexicon["/start"],
        reply_markup=await get_main_menu(state=state, lexicon=lexicon),
    )


@router.message(
    or_f(
        Command("donate"),
        F.text.lower() == "поддержать автора",
        F.text.lower() == "support the author",
    ),
    StateFilter(default_state),
)
async def donate_handler(message: Message, state: FSMContext):
    logger.debug("Пользователь отправил команду /donate")
    data = await state.get_data()
    lang = data.get("lexicon", "RU")
    lexicon = LEXICON_RU if lang == "RU" else LEXICON_EN
    await message.answer(lexicon["/donate"])


# Этот хэндлер срабатывает на команду /help
@router.message(
    or_f(
        Command("help"),
        F.text.lower() == "помощь",
        F.text.lower() == "help",
    ),
    StateFilter(default_state),
)
async def help_handler(message: Message, state: FSMContext):
    logger.debug("Пользователь отправил команду /help")
    data = await state.get_data()
    lang = data.get("lexicon", "RU")
    lexicon = LEXICON_RU if lang == "RU" else LEXICON_EN
    await message.answer(
        lexicon["/help"], reply_markup=await get_main_menu(state=state, lexicon=lexicon)
    )

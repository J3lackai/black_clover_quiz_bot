from aiogram import Router, F
from keyboards import get_main_menu
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from loguru import logger
from aiogram.fsm.state import default_state
from redis.asyncio import Redis


# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, redis: Redis, lexicon: dict[str:str]):
    logger.debug("Пользователь отправил команду start")
    passes = await redis.get(f"user:{message.from_user.id}:passes")
    passes = int(passes.decode()) if passes is not None else 0
    text_start = lexicon["restart"] if passes > 0 else lexicon["start"]
    await message.answer(
        text=text_start,
        reply_markup=get_main_menu(lexicon=lexicon),
    )


@router.message(
    or_f(
        Command("donate"),
        F.text == "Поддержать автора",
        F.text == "Support the author",
    ),
    StateFilter(default_state),
)
async def donate_handler(message: Message, lexicon: dict):
    logger.debug("Пользователь отправил команду donate")
    await message.answer(lexicon["donate"])


# Этот хэндлер срабатывает на команду help
@router.message(
    or_f(Command("help"), F.text == ("Помощь"), F.text == ("Help")),
    StateFilter(default_state),
)
async def help_handler(message: Message, lexicon: dict[str:str]):
    logger.debug("Пользователь отправил команду help")
    await message.answer(lexicon["help"], reply_markup=get_main_menu(lexicon=lexicon))

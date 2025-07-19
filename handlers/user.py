from aiogram import Router, F
from keyboards import get_main_menu
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter, or_f
from loguru import logger
from aiogram.fsm.state import default_state
from redis.asyncio import Redis
from keyboards import select_language
from lexicon import LEXICON_EN, LEXICON_RU

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду start
@router.message(CommandStart(), StateFilter(default_state))
async def start_cmd(message: Message, redis: Redis, lexicon: dict[str:str]):
    """
    Хендлер для обработки /start, либо знакомит пользователя с игрой, либо предлагает сыграть ещё раз
    """
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
        F.text == "Support the Author",
    ),
    StateFilter(default_state),
)
async def donate_cmd(message: Message, lexicon: dict):
    """
    Хендлер для обработки /donate
    """
    logger.debug("Пользователь отправил команду donate")
    await message.answer(lexicon["donate"])


# Этот хэндлер срабатывает на команду help
@router.message(
    or_f(Command("help"), F.text == ("Помощь"), F.text == ("Help")),
    StateFilter(default_state),
)
async def help_cmd(message: Message, lexicon: dict[str:str]):
    """
    Хендлер для обработки /help
    """
    logger.debug("Пользователь отправил команду help")
    await message.answer(lexicon["help"], reply_markup=get_main_menu(lexicon=lexicon))


@router.message(
    or_f(F.text == "Выбрать язык", F.text == "Choose Language"),
    StateFilter(default_state),
)
async def setup_lang_cmd(message: Message):
    """Хендлер для выдачи клавиатуры смены языка пользователю"""
    await message.answer(
        "Выберите язык / Select your language:",
        reply_markup=select_language(),
    )


@router.message(or_f(F.text == "RU", F.text == "EN"), StateFilter(default_state))
async def process_language_choice(message: Message, redis: Redis):
    """Хендлер для смены языка"""
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
    await start_cmd(message, redis, lexicon)

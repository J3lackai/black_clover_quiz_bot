from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon import LEXICON_RU, LEXICON_EN
from loguru import logger


def get_answers_keyboard(num_of_q: int, lang: str = "RU") -> ReplyKeyboardMarkup:
    """
    Возвращает клавиатуру с вариантами ответов для вопроса num_of_q
    :param num_of_q: номер вопроса
    :param lang: язык ('RU' или 'EN')
    :return: ReplyKeyboardMarkup
    """
    kb_builder = ReplyKeyboardBuilder()

    # Получаем нужный словарь по языку
    lexicon = LEXICON_RU if lang == "RU" else LEXICON_EN

    # Проверка наличия ключа
    answers_key = f"a{num_of_q}"
    if answers_key not in lexicon:
        logger.error(f"Отсутствующие ответы на вопрос {num_of_q} в LEXICON_{lang}")
        raise KeyError()

    buttons = [KeyboardButton(text=option) for option in lexicon[answers_key]]
    kb_builder.row(*buttons, width=4)
    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def select_language() -> ReplyKeyboardMarkup:
    """
    Клавиатура выбора языка
    """
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="RU"), KeyboardButton(text="EN")]],
        resize_keyboard=True,
        input_field_placeholder="Choose your language / Выберите язык",
    )

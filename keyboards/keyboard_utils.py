from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from random import shuffle


def get_answers_keyboard(num_of_q: int, lexicon: dict) -> ReplyKeyboardMarkup:
    """
    Возвращает клавиатуру с вариантами ответов для вопроса num_of_q
    :param num_of_q: номер вопроса
    :param lexicon: LEXICON_RU | LEXICON_EN
    :return: ReplyKeyboardMarkup
    """
    kb_builder = ReplyKeyboardBuilder()
    right_ch = lexicon[f"r{num_of_q}"]
    set_chs = lexicon["characters"]
    set_chs.discard(right_ch)
    buttons = list()
    buttons.append(KeyboardButton(text=right_ch))  # Кнопка с правильным персонажем
    for ch in set_chs:
        if len(buttons) == 10:
            break
        # Кнопки с рандомными персонажами
        buttons.append(KeyboardButton(text=ch))
    shuffle(
        buttons
    )  # Перемешали чтобы правильный персонаж был рандомной кнопкой, а не первой
    shuffle(buttons)
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

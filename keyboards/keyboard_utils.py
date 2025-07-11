from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon_ru import LEXICON_RU


def get_answers_keyboard(num_of_q: int) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text=LEXICON_RU["a" + str(num_of_q)][i]) for i in range(10)
    ]
    kb_builder.row(*buttons, width=4)
    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

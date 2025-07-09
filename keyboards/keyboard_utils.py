from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon_ru import LEXICON_RU


def get_answers_keyboard_quiz(num_of_q: int) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(KeyboardButton(text=LEXICON_RU["q" + str(num_of_q)]), width=4)

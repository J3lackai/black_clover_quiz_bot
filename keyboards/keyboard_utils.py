from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon_ru import LEXICON_RU


def get_answers_keyboard_quiz(options: list[str], num_of_q: int) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text=LEXICON_RU["q" + str(i)]) for i in range(1, 11)]
    kb_builder.row(*buttons, width=4)

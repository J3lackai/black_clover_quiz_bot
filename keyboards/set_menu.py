from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать квиз сначала")],
        [KeyboardButton(text="Помощь")],
        [KeyboardButton(text="Поддержать автора")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)

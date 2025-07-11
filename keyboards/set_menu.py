from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_buttons = ("Начать квиз сначала", "Помощь", "Поддержать автора")
main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=i)] for i in menu_buttons],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)

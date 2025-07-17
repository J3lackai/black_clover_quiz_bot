from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu(lexicon: dict[str:str]):
    menu_buttons = (
        lexicon["menu_start"],
        lexicon["menu_help"],
        lexicon["menu_donate"],
        lexicon["menu_settings"],
    )
    main_menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=i)] for i in menu_buttons],
        resize_keyboard=True,
        input_field_placeholder=lexicon["menu_choose_action"],
    )
    return main_menu

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext


async def get_main_menu(state: FSMContext, lexicon: dict):
    menu_buttons = (lexicon["menu_start"], lexicon["menu_help"], lexicon["menu_donate"])
    main_menu = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=i)] for i in menu_buttons],
        resize_keyboard=True,
        input_field_placeholder=lexicon["menu_choose_action"],
    )
    return main_menu

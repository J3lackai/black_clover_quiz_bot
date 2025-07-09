from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter, F
from lexicon.lexicon_ru import LEXICON_RU
from states.states import FSMFillForm
from aiogram.fsm.context import FSMContext
from keyboards import get_answers_keyboard, main_menu, state_map

# Инициализируем роутер уровня модуля
router = Router()


@router.message(StateFilter(FSMFillForm.wait_for))
async def proccess_start_command(message: Message):
    await message.answer(text=LEXICON_RU["Давай!"])


@router.message(StateFilter(*[s[0] for s in state_map.values()]))
async def process_question(message: Message, state: FSMContext):
    current_state = await state.get_state()
    state_name = current_state.split(":")[1]
    question_num = int(state_name[1:])
    question_key = f"q{question_num}"
    question_text = LEXICON_RU.get(question_key, "Вопрос не найден")
    keyboard = get_answers_keyboard(question_num)

    await message.answer(text=question_text, reply_markup=keyboard)

    # Переход к следующему состоянию
    next_state = state_map[question_num][1]
    if next_state:
        await state.set_state(next_state)
    else:
        await message.answer("Надеюсь вам понравился наш квиз!🤗")
        await state.clear()

    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.q2)


@router.message(F.text == "Начать квиз сначала")
async def restart_quiz(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FSMFillForm.q1)
    await message.answer("Квиз начинается...", reply_markup=main_menu)


@router.message(F.text == "Помощь")
async def help_handler(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU["/help"])


@router.message(F.text == "Поддержать автора")
async def donate_handler(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU["/donate"])


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(FSMFillForm.default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU["/start"])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands="help"), StateFilter(FSMFillForm.default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU["/help"])

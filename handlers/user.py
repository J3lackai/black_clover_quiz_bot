from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from lexicon.lexicon_ru import LEXICON_RU
from states.states import FSMFillForm
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from keyboards import get_answers_keyboard, main_menu, menu_buttons
from states.states import state_map

# Инициализируем роутер уровня модуля
router = Router()
counter = 0


@router.message(F.text == "Начать квиз сначала")
async def restart_quiz(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FSMFillForm.q1)
    await message.answer("Квиз начинается...")
    await process_question(message, state)


@router.message(StateFilter(FSMFillForm.f))
async def final_quiz(message: Message, state: FSMContext):
    data = await state.get_data()
    score = f"{data.get('score', 0) * 10}"

    async def process_result():
        if score == 10:
            await message.answer(
                LEXICON_RU["final_brilliant"] + score + LEXICON_RU["final_stmt"]
            )
        elif 6 <= score <= 9:
            await message.answer(
                LEXICON_RU["final_well"] + score + LEXICON_RU["final_stmt"]
            )
        else:
            await message.answer(
                LEXICON_RU["final_not_bad"] + score + LEXICON_RU["final_stmt"]
            )

    await state.clear()
    await state.set_state(FSMFillForm.q1)
    await process_result()
    data["score"] = 0
    await donate_handler(message)
    await state.clear()


@router.message(StateFilter(*[s[0] for s in state_map.values()]))
async def check_answer(message: Message, state: FSMContext):
    current_state = await state.get_state()
    state_name = current_state.split(":")[1]
    question_num = int(state_name[1:])

    correct_answer = LEXICON_RU.get(f"r{question_num}")
    user_answer = message.text.strip()

    data = await state.get_data()
    score = data.get("score", 0)

    if user_answer == correct_answer:
        score += 1
        await message.answer("✅ Верно! Так держать.")
    else:
        await message.answer(f"Это не так. Правильный ответ: {correct_answer}")

    await state.update_data(score=score)

    next_state = state_map[question_num][1]
    if next_state:
        await state.set_state(next_state)
        await process_question(message, state)


@router.message(StateFilter(*[s[0] for s in state_map.values()]))
async def process_question(message: Message, state: FSMContext):
    current_state = await state.get_state()
    state_name = current_state.split(":")[1]
    question_num = int(state_name[1:])
    question_key = f"q{question_num}"
    question_text = LEXICON_RU.get(question_key, "Вопрос не найден")
    keyboard = get_answers_keyboard(question_num)

    await message.answer(text=question_text, reply_markup=keyboard)


@router.message(F.text == "Помощь")
async def help_handler(message: Message):
    await message.answer(LEXICON_RU["/help"])


@router.message(F.text == "Поддержать автора")
async def donate_handler(message: Message):
    await message.answer(LEXICON_RU["/donate"])


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU["/start"], reply_markup=main_menu)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands="help"), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU["/help"])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands="donate"), StateFilter(default_state))
async def process_donate_command(message: Message):
    await message.answer(text=LEXICON_RU["/donate"])


# Этот хэндлер срабатывает на другие команды
@router.message()
async def process_unvalid_commands(message: Message):
    await message.answer(text=LEXICON_RU["unvalid"])

from aiogram.fsm.context import FSMContext
from keyboards import get_answers_keyboard
from states.states import state_map
from aiogram.types import Message, ReplyKeyboardRemove
from states.states import FSMFillForm
from aiogram import Router, F
from aiogram.filters import StateFilter
from lexicon import LEXICON_RU
from user import donate_handler

router = Router()


@router.message(F.text == "Начать квиз сначала")
async def restart_quiz(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FSMFillForm.q1)
    await message.answer("Квиз начинается...")
    await process_question(message, state)


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
    await state.set_state(next_state)
    if next_state == FSMFillForm.f:
        await final_quiz(message, state)
    await process_question(message, state)


async def process_question(message: Message, state: FSMContext):
    current_state = await state.get_state()
    state_name = current_state.split(":")[1]
    question_num = int(state_name[1:])
    question_key = f"q{question_num}"
    question_text = LEXICON_RU.get(question_key, "Вопрос не найден")
    keyboard = get_answers_keyboard(question_num)

    await message.answer(text=question_text, reply_markup=keyboard)


async def final_quiz(message: Message, state: FSMContext):
    data = await state.get_data()
    score = data.get("score", 0)
    percents = f"{score * 10}"

    async def process_print_result():
        if score == 10:
            await message.answer(LEXICON_RU["final_brilliant"])
        elif 6 <= score <= 9:
            await message.answer(LEXICON_RU["final_well"])
        else:
            await message.answer(LEXICON_RU["final_not_bad"])
        await message.answer(
            text=percents + LEXICON_RU["final_stmt"], reply_markup=ReplyKeyboardRemove()
        )

    await state.clear()
    await state.set_state(FSMFillForm.q1)
    await process_print_result()
    data["score"] = 0
    await donate_handler(message)
    await state.clear()

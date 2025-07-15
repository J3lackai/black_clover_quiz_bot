from aiogram.fsm.context import FSMContext
from keyboards import get_answers_keyboard
from states.states import state_map
from aiogram.types import Message, ReplyKeyboardRemove
from states.states import FSMFillForm
from aiogram import Router, F
from aiogram.filters import StateFilter, or_f
from handlers import donate_handler
from loguru import logger
from lexicon import LEXICON_EN, LEXICON_RU

router = Router()


@router.message(or_f(F.text == "Начать квиз сначала", F.text == "Start quiz again"))
async def restart_quiz(message: Message, state: FSMContext):
    logger.debug("Пользователь начал квиз заново...")
    await state.clear()
    await state.set_state(FSMFillForm.q1)
    data = await state.get_data()
    lexicon = LEXICON_RU if data.get("lexicon", "RU") == "RU" else LEXICON_EN
    await message.answer(lexicon["start_quiz"])
    await process_question(message, state)


@router.message(StateFilter(*[s[0] for s in state_map.values()]))
async def check_answer(message: Message, state: FSMContext):
    logger.debug("Идёт проверка ответа...")
    current_state = await state.get_state()
    state_name = current_state.split(":")[1]
    question_num = int(state_name[1:])
    data = await state.get_data()
    lexicon = LEXICON_RU if data.get("lexicon", "RU") == "RU" else LEXICON_EN
    correct_answer = lexicon[f"r{question_num}"]
    user_answer = message.text.strip()

    data = await state.get_data()
    score = data.get("score", 0)

    if user_answer == correct_answer:
        score += 1
        await message.answer(lexicon["you_right"])
    else:
        await message.answer(lexicon["oh_no"].format(correct_answer=correct_answer))

    await state.update_data(score=score)

    next_state = state_map[question_num][1]
    await state.set_state(next_state)
    if next_state == FSMFillForm.f:
        await final_quiz(message, state)
    await process_question(message, state)


async def process_question(message: Message, state: FSMContext):
    logger.debug("Даём очередную цитату пользователю...")
    data = await state.get_data()
    lang = data.get("lexicon", "RU")
    lexicon = LEXICON_RU if lang == "RU" else LEXICON_EN
    current_state = await state.get_state()
    if current_state is None:
        return
    state_name = current_state.split(":")[1]
    question_num = int(state_name[1:])
    question_key = f"q{question_num}"
    question_text = lexicon.get(question_key)
    keyboard = get_answers_keyboard(question_num, lang)

    await message.answer(text=question_text, reply_markup=keyboard)


async def final_quiz(message: Message, state: FSMContext):
    logger.debug("Пользователь прошёл квиз...")
    data = await state.get_data()
    lexicon = LEXICON_RU if data.get("lexicon", "RU") == "RU" else LEXICON_EN
    score = data.get("score", 0)
    percents = f"{score * 10}"

    async def process_print_result():
        if score == 10:
            await message.answer(lexicon["final_brilliant"])
        elif 6 <= score <= 9:
            await message.answer(lexicon["final_well"])
        else:
            await message.answer(lexicon["final_not_bad"])
        await message.answer(
            text=percents + lexicon["final_stmt"], reply_markup=ReplyKeyboardRemove()
        )

    await process_print_result()
    await donate_handler(message, state)
    await state.clear()

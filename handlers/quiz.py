from aiogram.fsm.context import FSMContext
from keyboards import get_answers_keyboard
from states.states import state_map
from aiogram.types import Message, ReplyKeyboardRemove
from states.states import FSMFillForm
from aiogram import Router, F
from aiogram.filters import StateFilter, or_f
from handlers import process_start_command
from loguru import logger
from redis.asyncio import Redis

router = Router()


@router.message(or_f(F.text == "Начать квиз сначала", F.text == "Start quiz again"))
async def restart_quiz(message: Message, state: FSMContext, lexicon: dict[str:str]):
    logger.debug("Пользователь начал квиз заново...")
    await state.set_state(FSMFillForm.q1)
    await message.answer(lexicon["start_quiz"])
    await process_question(message, state, lexicon)


@router.message(StateFilter(*[s[0] for s in state_map.values()]))
async def check_answer(
    message: Message, state: FSMContext, redis: Redis, lexicon: dict[str:str]
):
    logger.debug("Идёт проверка ответа...")
    current_state = await state.get_state()
    state_name = current_state.split(":")[1]
    question_num = int(state_name[1:])
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
        await final_quiz(message, state, redis, lexicon)
    await process_question(message, state, lexicon)


async def process_question(message: Message, state: FSMContext, lexicon: dict[str:str]):
    logger.debug("Даём очередную цитату пользователю...")
    current_state = await state.get_state()
    if current_state is None:
        return
    state_name = current_state.split(":")[1]
    question_num = int(state_name[1:])
    question_key = f"q{question_num}"
    question_text = lexicon.get(question_key)

    keyboard = get_answers_keyboard(question_num, lexicon)

    await message.answer(text=question_text, reply_markup=keyboard)


async def final_quiz(
    message: Message, state: FSMContext, redis: Redis, lexicon: dict[str:str]
):
    data = await state.get_data()
    passes = data.get("score", 0)
    percents = f"{passes * 10}"

    async def process_print_result():
        if passes == 10:
            await message.answer(lexicon["final_brilliant"])
        elif 6 <= passes <= 9:
            await message.answer(lexicon["final_well"])
        else:
            await message.answer(lexicon["final_not_bad"])
        await message.answer(
            text=percents + lexicon["final_stmt"], reply_markup=ReplyKeyboardRemove()
        )

    await process_print_result()
    passes = await redis.get(f"user:{message.from_user.id}:passes")
    passes = int(passes.decode()) if passes is not None else 0
    await redis.set(
        f"user:{message.from_user.id}:passes", passes + 1
    )  # Увеличили количество прохождений квиза для юзера
    logger.info(f"Пользователь {message.from_user.id} прошёл квиз {passes} раз :)")
    await state.clear()
    await process_start_command(message, redis, lexicon)

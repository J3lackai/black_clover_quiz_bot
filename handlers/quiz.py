from aiogram.fsm.context import FSMContext
from keyboards import get_answers_keyboard
from aiogram.types import Message, ReplyKeyboardRemove
from states import FSMFillForm as fsm, state_map
from aiogram import Router, F
from aiogram.filters import StateFilter, or_f
from handlers import start_cmd
from loguru import logger
from redis.asyncio import Redis

router = Router()


@router.message(or_f(F.text == "Начать квиз сначала", F.text == "Start Quiz Again"))
async def restart_quiz_cmd(
    message: Message, state: FSMContext, redis: Redis, lexicon: dict[str:str]
):
    """
    Хендлер для обработки случая когда пользователь начал квиз заново
    """
    logger.debug("Пользователь начал квиз заново...")
    await state.set_state(fsm.q1)
    await message.answer(lexicon["start_quiz"])
    await process_question_quiz(message, state, redis, lexicon)


@router.message(StateFilter(*[s[0] for s in state_map.values()]))
async def check_answer_quiz(
    message: Message, state: FSMContext, redis: Redis, lexicon: dict[str:str]
):
    """
    Хендлер для проверки ответа пользователя, вывода ему информации о правильном ответе,
    переход в следующее состояние или финальное
    """
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
    if next_state == fsm.f:
        await process_final_quiz(message, state, redis, lexicon)
    else:
        await process_question_quiz(message, state, redis, lexicon)


async def process_question_quiz(
    message: Message,
    state: FSMContext,
    redis: Redis,
    lexicon: dict[str:str],
):
    """
    Корутина для выдачи клавиатуры с именами персонажей пользователю
    """
    logger.debug("Даём очередную цитату пользователю...")
    current_state = await state.get_state()
    state_name = current_state.split(":")[1]
    question_num = int(state_name[1:])

    question_key = f"q{question_num}"
    question_text = lexicon.get(question_key)
    keyboard = get_answers_keyboard(question_num, lexicon)
    await message.answer(text=question_text, reply_markup=keyboard)
    await state.update_data(current_state=current_state)


async def process_final_quiz(
    message: Message, state: FSMContext, redis: Redis, lexicon: dict[str:str]
):
    """
    Корутина для завершения квиза, вывода результатов, сброса состояния
    """
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
    await start_cmd(message, redis, lexicon)

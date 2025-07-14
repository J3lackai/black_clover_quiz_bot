from lexicon import LEXICON_EN, LEXICON_RU
from aiogram.fsm.context import FSMContext


def chunk_list(lst: list, n: int) -> list[list]:
    return [lst[i : i + n] for i in range(0, len(lst), n)]


async def get_lexicon(state: FSMContext) -> tuple[dict, bool]:
    data = await state.get_data()
    flag_not_set = True
    try:
        lexicon = await data.get("lexicon")
        flag_not_set = False
    except KeyError:
        lexicon = "RU"
    return LEXICON_RU, flag_not_set if lexicon == "RU" else LEXICON_EN, flag_not_set

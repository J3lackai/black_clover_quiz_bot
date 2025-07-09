# from aiogram import Bot, Dispatcher, F
# from aiogram.filters import Command, CommandStart, StateFilter
# from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup  # default_state
from aiogram.fsm.storage.memory import MemoryStorage
from states.states import FSMFillForm

state_map = {
    1: (FSMFillForm.q1, FSMFillForm.q2),
    2: (FSMFillForm.q2, FSMFillForm.q3),
    3: (FSMFillForm.q3, FSMFillForm.q4),
    4: (FSMFillForm.q4, FSMFillForm.q5),
    5: (FSMFillForm.q5, FSMFillForm.q6),
    6: (FSMFillForm.q6, FSMFillForm.q7),
    7: (FSMFillForm.q7, FSMFillForm.q8),
    8: (FSMFillForm.q8, FSMFillForm.q9),
    9: (FSMFillForm.q9, FSMFillForm.q10),
    10: (FSMFillForm.q10, FSMFillForm.f),
}
storage = MemoryStorage()


class FSMFillForm(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
    f = State()

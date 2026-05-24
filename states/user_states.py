from aiogram.fsm.state import (
    StatesGroup,
    State
)


class UserStates(StatesGroup):

    waiting_link = State()

    choosing_media = State()

    processing = State()
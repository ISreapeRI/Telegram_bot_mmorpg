from aiogram.dispatcher.filters.state import State, StatesGroup


class Registry(StatesGroup):
    name = State()
    gender = State()
    first_element = State()
    last = State()


class education(StatesGroup):
    pass


class step_movement(StatesGroup):
    init = State()
    right_step = State()
    left_step = State()
    upper_step = State()
    down_step = State()


class map_movement(StatesGroup):
    movement = State()

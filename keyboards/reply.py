from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def gender():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton('Мужской'),
                KeyboardButton('Женский')
            ]
        ],
        resize_keyboard=True
    )

    return keyboard


def first_element():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton('Огонь'),
                KeyboardButton('Вода')
            ],
            [
                KeyboardButton('Земля'),
                KeyboardButton('Воздух')
            ]
        ],
        resize_keyboard=True
    )

    return keyboard


def education_start():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton('Начать обучение')]
        ],
        resize_keyboard=True
    )

    return keyboard


def return_to_map():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton('Вернуться на карту')]
        ],
        resize_keyboard=True
    )

    return keyboard


def interact_with_npc(name):
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton('Поговорить c ' + name)]
        ],
        resize_keyboard = True
    )

    return keyboard
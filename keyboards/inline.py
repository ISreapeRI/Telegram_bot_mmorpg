from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_element():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Огонь", callback_data = "start:fire"),
                InlineKeyboardButton("Вода", callback_data = "start:water")
            ],

            [
                InlineKeyboardButton("Земля", callback_data = "start:earth"),
                InlineKeyboardButton("Воздух", callback_data = "start:wind")
            ]
        ]
    )

    return keyboard


def movement():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton('↑', callback_data = 'up')
            ],
            [
                InlineKeyboardButton('←', callback_data = 'left'),
                InlineKeyboardButton('n', callback_data = 'n'),
                InlineKeyboardButton('→', callback_data = 'right')
            ],
            [
                InlineKeyboardButton('↓', callback_data = 'down')
            ]
        ]
    )

    return keyboard


def n_movement():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton('↑', callback_data='up')
            ],
            [
                InlineKeyboardButton('←', callback_data='left'),
                InlineKeyboardButton('Назад', callback_data='back'),
                InlineKeyboardButton('→', callback_data='right')
            ],
            [
                InlineKeyboardButton('↓', callback_data='down')
            ]
        ]
    )

    return keyboard


def sendGameKeyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton('launch game', callback_data = 'launch_check')
            ]
        ]
    )

    return keyboard
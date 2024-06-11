import sqlite3

from aiogram import types
from aiogram.dispatcher.filters import CommandStart

import functions.map_drawing as map

from loader import users, users_db, bot

from keyboards import inline
from loader import dp
from states import Registry


@dp.message_handler(commands= ['refresh'], state= "*")
async def refresh(message: types.Message):
    print("refresh")
    with open(map.map_drawing(message.from_user.id), 'rb') as photo:
        await message.answer_photo(photo, reply_markup=inline.movement())


@dp.message_handler(commands = ['game'], state = "*")
async def sendGame(message: types.Message):

    await bot.send_game(message.chat.id, 'NewElementGame')


@dp.message_handler(CommandStart(), state= "*")
async def start(message: types.Message):
    print('hello')
    try:
        users.execute("insert into users (user_id, full_name, chat_id) values (?, ?, ?)",
                      (message['from']['id'], message.from_user.full_name, message.chat.id))
        users_db.commit()
        await Registry.name.set()
        await message.answer(f'Приветствую, {message.from_user.full_name}!'
                             f'\nТы попал в мир игры New Element!'
                             f'\n\nДавай создадим твоего персонажа, чтобы твои приключения наконец-то начались!'
                             f'\nДля начала, выбери имя, под которым тебя будут узнавать.'
                             f'\nНо лучше чтобы оно было на английском, а то на русском как-то просто будет')
    except sqlite3.IntegrityError:
        name = users.execute(f'select nickname from users where user_id = {message["from"]["id"]}').fetchall()[0][0]
        if name is None:
            await message.answer("Пожалуйста, завершите регистрацию.")
        else:
            await message.answer("Извините, но вы уже зарегестрированы.")


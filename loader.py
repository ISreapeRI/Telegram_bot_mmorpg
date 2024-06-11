import asyncio
import sqlite3

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from states import map_movement, step_movement

users_db = sqlite3.connect("datas/users.db")
users = users_db.cursor()

list_of_actions = ['npc']

memory = MemoryStorage()
bot = Bot(token = open("token.txt", "r").read())
dp = Dispatcher(bot, storage = memory)


def set_state():
    start = asyncio.new_event_loop()
    start.run_until_complete(states())


async def states():
    list_of_players = users.execute('select user_id from users').fetchall()
    for i in list_of_players:
        state = dp.current_state(user=i[0])
        await state.set_state(map_movement.movement)

import asyncio
import logging
import sqlite3


from aiogram import executor

# -- основная инициализация --

from loader import set_state
from handlers import dp

logging.basicConfig(level=logging.INFO)

# -- запуск пуллинга --

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=set_state())

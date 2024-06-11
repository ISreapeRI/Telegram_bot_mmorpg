import sqlite3
from aiogram.dispatcher import FSMContext
from functions.map_drawing import map_drawing
from loader import dp
from keyboards import inline, reply
from loader import users, users_db
from aiogram import types
from states import Registry, step_movement, map_movement


@dp.message_handler(text = 'Вернуться на карту', state = "*")
async def back_to_map(message: types.Message, state: FSMContext):
    await state.finish()
    await map_movement.movement.set()
    await message.answer('Возвращаемся к карте')

    with open(map_drawing(message.from_user.id), 'rb') as photo:
        await message.edit_reply_markup(inline.movement())
        await message.answer_photo(photo, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: not message.text.isdigit(), state = step_movement.all_states)
async def digit_error(message: types.Message):
    await message.answer('Введите число!')


@dp.message_handler(state = step_movement.left_step)
async def step_movement_not_invalid(message: types.Message):
    await message.answer("ты ввел число")


@dp.message_handler(state = step_movement.right_step)
async def step_movement_not_invalid(message: types.Message):
    await message.answer("ты ввел число")


@dp.message_handler(state = step_movement.down_step)
async def step_movement_not_invalid(message: types.Message):
    await message.answer("ты ввел число")


@dp.message_handler(state = step_movement.upper_step)
async def step_movement_not_invalid(message: types.Message):
    await message.answer("ты ввел число")


@dp.message_handler(state=Registry.name)
async def registry(message: types.Message):
    try:
        users.execute('update users set nickname = (?) where user_id = (?)', (message.text, message['from']['id']))
        users_db.commit()
        await Registry.next()
        await message.answer('Отлично, теперь о твоем имени будут слагать легенды, уж поверь мне!'
                             '\nДавай выберем пол твоего персонажа.',
                             reply_markup=reply.gender())
    except sqlite3.IntegrityError:
        await message.answer('Такое имя уже занято. Попробуй еще раз.')


@dp.message_handler(lambda message: message.text not in ['Мужской', 'Женский'], state=Registry.gender)
async def gender_not_invalid(message: types.Message):
    await message.answer('Нет такого пола. Выбери пол, нажав на одну из кнопок снизу!')


@dp.message_handler(state=Registry.gender)
async def gender(message: types.Message):
    users.execute('update users set gender = (?) where user_id = (?)', (message.text, message.from_user.id))
    users_db.commit()
    await Registry.next()
    await message.answer('Отлично! Теперь остался последний этап.'
                         '\nВыбери свой первый элемент, но не беспокойся, остальные ты тоже сможешь получить!'
                         '\nТвой первый элемент будет вляить только на то, как начнется твое приключение!',
                         reply_markup=reply.first_element())


@dp.message_handler(lambda message: message.text not in ['Огонь', 'Вода', 'Земля', 'Воздух'],
                    state=Registry.first_element)
async def first_element_not_invalid(message: types.Message):
    await message.answer('Выбери одну из кнопок снизу!')


@dp.message_handler(state=Registry.first_element)
async def first_element(message: types.Message):
    users.execute('update users set element_1 = (?) where user_id = (?)', (message.text, message.from_user.id))

    if message.text == 'Огонь':
        users.execute('update users set location = (?) where user_id = (?)', ('start_wind', message.from_user.id))
    elif message.text == 'Вода':
        users.execute('update users set location = (?) where user_id = (?)', ('start_wind', message.from_user.id))
    elif message.text == 'Земля':
        users.execute('update users set location = (?) where user_id = (?)', ('start_wind', message.from_user.id))
    elif message.text == 'Воздух':
        users.execute('update users set location = (?) where user_id = (?)', ('start_wind', message.from_user.id))

    users_db.commit()
    await Registry.next()
    await message.answer('Теперь нажми кнопку "Начать обучение", чтобы начать свое незабываемое приключение!',
                         reply_markup=reply.education_start())


@dp.message_handler(text='Начать обучение', state='*')
async def need_education(message: types.Message):
    await map_movement.movement.set()
    await message.answer('Создание обучения', reply_markup=types.ReplyKeyboardRemove())

    location = users.execute(f'select location from users where user_id = {message.from_user.id}').fetchone()[0]
    nickname = users.execute(f'select nickname from users where user_id = {message.from_user.id}').fetchone()[0]

    users.execute('insert into users_start_wind (chat_id, nickname, user_id) values (?, ?, ?)',
                  (message.chat.id, nickname, message.from_user.id))
    users_db.commit()

    with open(map_drawing(message.from_user.id), 'rb') as photo:
        await message.answer_photo(photo, reply_markup = inline.movement())

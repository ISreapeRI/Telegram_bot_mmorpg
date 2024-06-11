from aiogram import types

from aiogram.dispatcher import FSMContext

from functions.map_drawing import map_drawing
from maps import maps

from keyboards import inline, reply
from loader import dp, users, users_db, list_of_actions, bot
from states import step_movement, map_movement


@dp.callback_query_handler(text='left', state=step_movement.init)
async def step_right_mode(query: types.CallbackQuery):
    await query.message.answer('Введите число шагов, которые хотели бы пройти', reply_markup=reply.return_to_map())
    await step_movement.left_step.set()


@dp.callback_query_handler(text='right', state=step_movement.init)
async def step_right_mode(query: types.CallbackQuery):
    await query.message.answer('Введите число шагов, которые хотели бы пройти', reply_markup=reply.return_to_map())
    await step_movement.right_step.set()


@dp.callback_query_handler(text='up', state=step_movement.init)
async def step_right_mode(query: types.CallbackQuery):
    await query.message.answer('Введите число шагов, которые хотели бы пройти', reply_markup=reply.return_to_map())
    await step_movement.upper_step.set()


@dp.callback_query_handler(text='down', state=step_movement.init)
async def step_right_mode(query: types.CallbackQuery):
    await query.message.answer('Введите число шагов, которые хотели бы пройти', reply_markup=reply.return_to_map())
    await step_movement.down_step.set()


@dp.callback_query_handler(text='n', state=map_movement.movement)
async def n_move(query: types.CallbackQuery):
    await query.answer('Пока что эта кнопка не работает')
    # await step_movement.init.set()
    # await query.message.edit_reply_markup(inline.n_movement())


@dp.callback_query_handler(text='back', state=step_movement.init)
async def not_n_move(query: types.CallbackQuery):
    await query.answer()
    await map_movement.movement.set()
    await query.message.edit_reply_markup(inline.movement())


@dp.callback_query_handler(text='right', state=map_movement.movement)
async def right_move(query: types.CallbackQuery):
    location = users.execute(f'select location from users where user_id = {query.from_user.id}').fetchone()[0]
    coords = users.execute(f'select x, y from {"users_" + location} where user_id = {query.from_user.id}').fetchone()
    users.execute(f'update users set rotate = "right" where user_id = {query.from_user.id}')

    if 'right' in maps[location].map[coords[0]][coords[1]]:
        users.execute(f'delete from {"users_" + location} where user_id = {query.from_user.id}')

        location_ = maps[location].map[coords[0]][coords[1]]['right']
        users.execute('update users set location = (?) where user_id = (?)', (location_, query.from_user.id))

        users.execute(f'insert into {"users_" + location_} (chat_id, nickname, user_id) values (?, ?, ?)',
                      (query.message.chat.id, coords[2], query.from_user.id))

        users.execute(
            f'update {"users_" + location_} set x = {maps[location].map[coords[0]][coords[1]]["xy"][0]} where user_id = {query.from_user.id}')
        users.execute(
            f'update {"users_" + location_} set y = {maps[location].map[coords[0]][coords[1]]["xy"][1]} where user_id = {query.from_user.id}')

        users_db.commit()

        with open(map_drawing(query.from_user.id), 'rb') as photo:
            photo = types.InputMediaPhoto(photo)
            await query.answer()
            await query.message.edit_media(photo, reply_markup=inline.movement())
            return
    else:
        if coords[0] + 1 > 19:
            await query.answer('Справа стена')
            return

        elif maps[location].map[coords[0] + 1][coords[1]]['wall']:
            await query.answer('Справа стена')

        object_count = 0
        objects_around = []
        for object in list_of_actions:
            if object in maps[location].map[coords[0] + 2][coords[1]]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0] + 2][coords[1]][object])
            if object in maps[location].map[coords[0]][coords[1]]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0]][coords[1]][object])
            if object in maps[location].map[coords[0] + 1][coords[1] + 1]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0] + 1][coords[1] + 1][object])
            if object in maps[location].map[coords[0] + 1][coords[1] - 1]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0] + 1][coords[1] - 1][object])

        if object_count == 1:
            print(objects_around)

            # await query.message.edit_reply_markup(reply_markup=reply.interact_with_npc(objects_around[0]['name']))
            with open(map_drawing(query.from_user.id), 'rb') as photo:
                await query.message.delete()
                new_mes = await query.message.answer_photo(photo, reply_markup=reply.interact_with_npc(objects_around[0]['name']))
                print(new_mes)
                users.execute(f'update {"users_" + location} set x = x + 1 where user_id = {query.from_user.id}')
                users_db.commit()
                with open(map_drawing(query.from_user.id), 'rb') as new_photo:
                    new_photo = types.InputMediaPhoto(new_photo)
                    await bot.edit_message_media(media = new_photo, chat_id = query.message.chat.id, message_id = new_mes.message_id, reply_markup = inline.movement())
                await query.answer()
                # await query.message.edit_media(photo, reply_markup=inline.movement())
                return
        elif object_count >= 2:
            print(objects_around)

    users.execute(f'update {"users_" + location} set x = x + 1 where user_id = {query.from_user.id}')
    users_db.commit()

    with open(map_drawing(query.from_user.id), 'rb') as photo:
        photo = types.InputMediaPhoto(photo)
        await query.answer()
        await query.message.edit_media(photo, reply_markup=inline.movement())


# --- Стандартное передвижение через кнопку направления влево ---


@dp.callback_query_handler(text='left', state=map_movement.movement)
async def left_move(query: types.CallbackQuery):
    location = users.execute(f'select location from users where user_id = {query.from_user.id}').fetchone()[0]
    coords = users.execute(f'select x, y from {"users_" + location} where user_id = {query.from_user.id}').fetchone()
    users.execute(f'update users set rotate = "left" where user_id = {query.from_user.id}')

    if 'left' in maps[location].map[coords[0]][coords[1]]:
        users.execute(f'delete from {"users_" + location} where user_id = {query.from_user.id}')

        location_ = maps[location].map[coords[0]][coords[1]]['left']
        users.execute('update users set location = (?) where user_id = (?)', (location_, query.from_user.id))

        users.execute(f'insert into {"users_" + location_} (chat_id, nickname, user_id) values (?, ?, ?)',
                      (query.message.chat.id, coords[2], query.from_user.id))

        users.execute(
            f'update {"users_" + location_} set x = {maps[location].map[coords[0]][coords[1]]["xy"][0]} where user_id = {query.from_user.id}')
        users.execute(
            f'update {"users_" + location_} set y = {maps[location].map[coords[0]][coords[1]]["xy"][1]} where user_id = {query.from_user.id}')

        users_db.commit()

        with open(map_drawing(query.from_user.id), 'rb') as photo:
            photo = types.InputMediaPhoto(photo)
            await query.answer()
            await query.message.edit_media(photo, reply_markup=inline.movement())
            return None
    else:
        if coords[0] - 1 < 0:
            await query.answer('Слева стена')
            return None

        elif maps[location].map[coords[0] - 1][coords[1]]['wall']:
            await query.answer('Слева стена')
            return None

        objects_around = []
        object_count = 0
        for object in list_of_actions:
            if object in maps[location].map[coords[0]][coords[1]]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0]][coords[1]][object])
            if object in maps[location].map[coords[0] - 2][coords[1]]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0] - 2][coords[1]][object])
            if object in maps[location].map[coords[0] - 1][coords[1] + 1]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0] - 1][coords[1] + 1][object])
            if object in maps[location].map[coords[0] - 1][coords[1] - 1]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0] - 1][coords[1] - 1][object])

        if object_count == 1:
            print(objects_around)
            await query.message.edit_reply_markup(reply_markup=reply.interact_with_npc(objects_around[0]['name']))
        elif object_count >= 2:
            print(objects_around)

    users.execute(f'update {"users_" + location} set x = x - 1 where user_id = {query.from_user.id}')
    users_db.commit()

    with open(map_drawing(query.from_user.id), 'rb') as photo:
        photo = types.InputMediaPhoto(photo)
        await query.answer()
        await query.message.edit_media(photo, reply_markup=inline.movement())


# --- Стандартное передвижение через кнопку направления вверх ---


@dp.callback_query_handler(text='up', state=map_movement.movement)
async def upper_move(query: types.CallbackQuery):
    location = users.execute(f'select location from users where user_id = {query.from_user.id}').fetchone()[0]
    coords = users.execute(
        f'select x, y, nickname from {"users_" + location} where user_id = {query.from_user.id}').fetchone()
    users.execute(f'update users set rotate = "up" where user_id = {query.from_user.id}')

    if 'up' in maps[location].map[coords[0]][coords[1]]:
        users.execute(f'delete from {"users_" + location} where user_id = {query.from_user.id}')

        location_ = maps[location].map[coords[0]][coords[1]]['up']
        users.execute('update users set location = (?) where user_id = (?)', (location_, query.from_user.id))

        users.execute(f'insert into {"users_" + location_} (chat_id, nickname, user_id) values (?, ?, ?)',
                      (query.message.chat.id, coords[2], query.from_user.id))

        users.execute(
            f'update {"users_" + location_} set x = {maps[location].map[coords[0]][coords[1]]["xy"][0]} where user_id = {query.from_user.id}')
        users.execute(
            f'update {"users_" + location_} set y = {maps[location].map[coords[0]][coords[1]]["xy"][1]} where user_id = {query.from_user.id}')

        users_db.commit()

        with open(map_drawing(query.from_user.id), 'rb') as photo:
            photo = types.InputMediaPhoto(photo)
            await query.answer()
            await query.message.edit_media(photo, reply_markup=inline.movement())
            return None
    else:
        if coords[1] - 1 < 0:
            await query.answer('Сверху стена')
            return None

        elif maps[location].map[coords[0]][coords[1] - 1]['wall']:
            await query.answer('Сверху стена')
            return None

        objects_around = []
        object_count = 0
        for object in list_of_actions:
            if object in maps[location].map[coords[0] + 1][coords[1] - 1]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0] + 1][coords[1] - 1][object])
            if object in maps[location].map[coords[0] - 1][coords[1] - 1]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0] - 1][coords[1] - 1][object])
            if object in maps[location].map[coords[0]][coords[1] - 2]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0]][coords[1] - 2][object])
            if object in maps[location].map[coords[0]][coords[1]]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0]][coords[1]][object])

        if object_count == 1:
            print(objects_around)
            await query.message.edit_reply_markup(reply_markup=reply.interact_with_npc(objects_around[0]['name']))
        elif object_count >= 2:
            print(objects_around)

    users.execute(f'update {"users_" + location} set y = y - 1 where user_id = {query.from_user.id}')
    users_db.commit()

    with open(map_drawing(query.from_user.id), 'rb') as photo:
        photo = types.InputMediaPhoto(photo)
        await query.answer()
        await query.message.edit_media(photo, reply_markup=inline.movement())


@dp.callback_query_handler(text='down', state=map_movement.movement)
async def down_move(query: types.CallbackQuery):
    location = users.execute(f'select location from users where user_id = {query.from_user.id}').fetchone()[0]
    coords = users.execute(
        f'select x, y, nickname from {"users_" + location} where user_id = {query.from_user.id}').fetchone()
    users.execute(f'update users set rotate = "down" where user_id = {query.from_user.id}')

    if 'down' in maps[location].map[coords[0]][coords[1]]:
        users.execute(f'delete from {"users_" + location} where user_id = {query.from_user.id}')

        location_ = maps[location].map[coords[0]][coords[1]]['down']
        users.execute('update users set location = (?) where user_id = (?)', (location_, query.from_user.id))

        users.execute(f'insert into {"users_" + location_} (chat_id, nickname, user_id) values (?, ?, ?)',
                      (query.message.chat.id, coords[2], query.from_user.id))

        users.execute(
            f'update {"users_" + location_} set x = {maps[location].map[coords[0]][coords[1]]["xy"][0]} where user_id = {query.from_user.id}')
        users.execute(
            f'update {"users_" + location_} set y = {maps[location].map[coords[0]][coords[1]]["xy"][1]} where user_id = {query.from_user.id}')

        users_db.commit()

        with open(map_drawing(query.from_user.id), 'rb') as photo:
            photo = types.InputMediaPhoto(photo)
            await query.answer()
            await query.message.edit_media(photo, reply_markup=inline.movement())

        return None
    else:
        if coords[1] + 1 > 19:
            await query.answer('Снизу стена')
            return

        elif maps[location].map[coords[0]][coords[1] + 1]['wall']:
            await query.answer('Снизу стена')
            return

        objects_around = []
        object_count = 0
        for object in list_of_actions:
            if object in maps[location].map[coords[0] + 1][coords[1] + 1]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0] + 1][coords[1] + 1][object])
            if object in maps[location].map[coords[0] - 1][coords[1] + 1]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0] - 1][coords[1] + 1][object])
            if object in maps[location].map[coords[0]][coords[1] + 2]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0]][coords[1] + 2][object])
            if object in maps[location].map[coords[0]][coords[1]]:
                object_count += 1
                objects_around.append(maps[location].map[coords[0]][coords[1]][object])

        if object_count == 1:
            print(objects_around)
            await query.message.edit_reply_markup(reply_markup=reply.interact_with_npc(objects_around[0]['name']))
        elif object_count >= 2:
            print(objects_around)

    users.execute(f'update {"users_" + location} set y = y + 1 where user_id = {query.from_user.id}')
    users_db.commit()

    with open(map_drawing(query.from_user.id), 'rb') as photo:
        photo = types.InputMediaPhoto(photo)
        await query.answer()
        await query.message.edit_media(photo, reply_markup=inline.movement())


@dp.callback_query_handler(state="*")
async def checkCallback(query: types.CallbackQuery):
    print('Кто-то вошел на сайт')
    if query.game_short_name == 'NewElementGame':
        await query.answer(url='https://e827-62-148-157-159.ngrok.io')
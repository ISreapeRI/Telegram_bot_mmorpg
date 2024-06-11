from typing import Union

from PIL import Image
from PIL.ImageDraw import ImageDraw

from loader import users, users_db


def map_drawing(user_id: Union[int]):
    location = users.execute(f'select location from users where user_id = {user_id}').fetchone()[0]

    coords = users.execute(f'select x, y, nickname from {"users_" + location}').fetchall()

    map = Image.open(f'maps/{location}/{location}_map.jpg')
    map_draw = ImageDraw(map)

    for i in coords:
        map_draw.rectangle([(i[0] * 50, i[1] * 50), (i[0] * 50 + 50, i[1] * 50 + 50)], fill='red')
    for i in coords:
        map_draw.text((i[0] * 50, (i[1] - 0.5) * 50), i[2])

    link = f'maps/{location}/new_{location}_map.jpg'
    map.save(link)

    return link
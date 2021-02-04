import sqlite3

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

vk_session = vk_api.VkApi(token="da3c917417e008d6f650f050a8b00c6ab0c4f84b3ff3f6a921890fe83445943508625a6e57c97b4f7c7cb")

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

con = sqlite3.connect("BotSJ.db")
cur = con.cursor()

initial_words = ['привет', 'приветик', 'начать', "помощь", "старт", "команды"] # потом дозаполню стартовый список
# список команд
command = '''Создать новый класс 'название класса', 'пароль'
Добавиться в класс 'имя класса' 'пароль'
Рассписание
'''


def write_msg(user_id, message):
    vk.messages.send(
        user_id=user_id,

        random_id=get_random_id(),
        message=message
    )

# основной код тут, sqlite3 почему-то ничего не сохраняют
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        request = event.text
        request = request.strip().lower()
        print(event.user_id)
        result = str(cur.execute(f'''SELECT user_id FROM users
    WHERE user_id = '{event.user_id}' ''').fetchall())[2:-3]
        print(result)
        if result != str(event.user_id):
            cur.execute(f'''INSERT INTO users(user_id, group_id) VALUES({event.user_id}, 'new_user') ''')
            write_msg(event.user_id, 'Хотите создать новый класс или присоединиться к другому?')

        elif request in initial_words:
            write_msg(event.user_id, command)

        elif 'создать новый класс' in request:
            group_id, password = request.replace('создать новый класс ', '').split(', ')
            print(group_id)
            print(password)
            result = str(cur.execute(f'''SELECT 1 FROM groups
                WHERE group_id = '{group_id}' ''').fetchall())[2:-3]
            print(result, '111111111')
            if result != '1':
                cur.execute(f'''INSERT INTO groups(group_id, password) VALUES('{group_id}', '{password}') ''')
                cur.execute(f'''UPDATE users SET group_id = '{group_id}' WHERE user_id = '{event.user_id}' ''')



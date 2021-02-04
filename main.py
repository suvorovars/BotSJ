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

# основной код тут
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
            con.commit()

        elif request in initial_words:
            write_msg(event.user_id, command)

        elif 'создать новый класс' in request:
            write_msg(event.user_id, 'в процессе')
            a = request.replace('создать новый класс ', '').split(', ')
            print(a)
            group_id, password = a
            print(group_id)
            print(password)
            result = str(cur.execute(f'''SELECT group_id FROM groups
                WHERE group_id = '{group_id}' ''').fetchall())[2:-2]
            print(result, '1')
            if result == '':
                cur.execute(f'''INSERT INTO groups(group_id, password) VALUES('{group_id}', '{password}') ''')
                cur.execute(f'''UPDATE users SET group_id = '{group_id}' WHERE user_id = '{event.user_id}' ''')
                cur.execute(f'''CREATE TABLE {group_id} (
    ID      INT
    call    STRING,
    monday  STRING,
    tuesday STRING,
    wednesday STRING,
    thursday STRING
    friday STRING); ''')
                con.commit()
                result = str(cur.execute(f'''SELECT user_id, group_id FROM users
                    WHERE user_id = '{event.user_id}' ''').fetchall())[2:-2]
                print(result)

        # пока не работает
        if 'новые звонки:' in request:
            a = request.replace('новые звонки: ', '').split(', ')
            result = str(cur.execute(f'''SELECT group_id FROM users
                            WHERE user_id = '{event.user_id}' ''').fetchall())[2:-2]
            cur.execute(f'''UPDATE {result} SET ID = 0, call = '' WHERE ''')
            for i in range(len(a)):
                cur.execute(f'''INSERT INTO {result}(ID, call) VALUES({i + 1}, '{a[i]}')''')




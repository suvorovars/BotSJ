import sqlite3

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from sql_requests import *

vk_session = vk_api.VkApi(token="da3c917417e008d6f650f050a8b00c6ab0c4f84b3ff3f6a921890fe83445943508625a6e57c97b4f7c7cb")

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

con = sqlite3.connect("BotSJ.db")
cur = con.cursor()

initial_words = ['привет', 'приветик', 'начать', "помощь", "старт", "команды", "да"] # потом дозаполню стартовый список
# список команд
command = '''
Добавиться в класс "Класс", "Пароль"
Рассписание 
'''
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

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
        result = user_presence(event.user_id)
        if not result:
            user_add(event.user_id)
            write_msg(event.user_id, 'Хотите создать новый класс или присоединиться к другому?')

        if request in initial_words:
            write_msg(event.user_id, command)

        elif 'новый класс' in request:
            write_msg(event.user_id, 'в процессе')
            a = request.replace('новый класс ', '').split(', ')
            group_id, password = a
            print(group_id)
            print(password)
            a = new_class(event.user_id, group_id, password)
            if a:
                write_msg(event.user_id, f'новый класс {group_id} с паролем {password} создан')
            else:
                write_msg(event.user_id, f'класс с названием {group_id} уже создан или некорректно назван')

        # пока не работает
        elif 'новые звонки:' in request:
            a = request.replace('новые звонки: ', '').split(', ')
            result = str(cur.execute(f'''SELECT group_id FROM users
                            WHERE user_id = '{event.user_id}' ''').fetchall())[2:-2]
            cur.execute(f'''UPDATE {result} 
    SET ID = 0, call = '' 
    WHERE ID != '' ''')
            for i in range(len(a)):
                cur.execute(f'''INSERT INTO {result}(ID, call) VALUES({i + 1}, '{a[i]}')''')

        elif request == 'расписание':
            mess = ''
            group_id = str(cur.execute(f'''SELECT group_id FROM users WHERE user_id = '{event.user_id}' ''').fetchall())[2:-3]
            print(group_id)
            for i in days:
                rasp = cur.execute(f'''SELECT {i} FROM {group_id} ''').fetchall()
                for i in rasp:
                    print(i)
                    mess = mess + str(i)[2:-3] + '\n'
                write_msg(event.user_id, mess)
                mess = ''


        elif 'добавиться в класс ' in request:
            write_msg(event.user_id, 'в процессе')
            a = request.replace('добавиться в класс ', '').split(', ')
            group_id, password = a
            result = str(cur.execute(f"SELECT 1 FROM groups WHERE group_id = '{group_id}' AND password = '{password}' ").fetchall())[2:-3]
            print(result)
            if result == '1':
                cur.execute(f"UPDATE users SET group_id = '{group_id}' WHERE user_id = '{event.user_id}' ")
                con.commit()
                write_msg(event.user_id, f'Вы присоединены к классу {group_id}')

        else:
            write_msg(event.user_id, 'Бот еще пока на стадии разработки, но вы можете отправить своё мнение в гугл форму: https://docs.google.com/forms/d/e/1FAIpQLSdmE-1tzm7v40qQW0RKq4bLMjHWE2TuwGpAypjxfZ5lf4csGw/viewform?usp=sf_link')







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
Добавиться "Класс", "Пароль"
Новый класс [6] "Класс", "Пароль"
Рассписание 
'''
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
days_ru = ['понедельник', 'вторник', 'среда', 'четверг', '', '']

def write_msg(user_id, message):
    vk.messages.send(
        user_id=user_id,

        random_id=get_random_id(),
        message=message
    )

# основной код тут

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        print(event.user_id)
        request = event.text
        request = request.strip().lower()
        if user_presence(event.user_id):
            user_add(event.user_id)
            write_msg(event.user_id, 'Хотите создать новый класс или присоединиться к другому?')

        if request in initial_words:
            write_msg(event.user_id, command)

        elif 'новый класс ' in request:
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

        elif 'новый класс 6' in request:
            write_msg(event.user_id, 'в процессе')
            a = request.replace('новый класс 6', '').split(', ')
            group_id, password = a
            print(group_id)
            print(password)
            a = new_class(event.user_id, group_id, password, sixday=True)
            if a:
                write_msg(event.user_id, f'новый класс {group_id} с паролем {password} создан')
            else:
                write_msg(event.user_id, f'класс с названием {group_id} уже создан или некорректно назван')

        elif 'изменить звонки:' in request:
            a = request.replace('изменить звонки: ', '').split(', ')
            result = str(cur.execute(f'''SELECT group_id FROM users
                            WHERE user_id = '{event.user_id}' ''').fetchall())[2:-2]
            update_journal(event.user_id, a, 'call')

        elif 'изменить понедельник:' in request:
            a = request.replace('изменить понедельник: ', '').split(', ')
            result = str(cur.execute(f'''SELECT group_id FROM users
                            WHERE user_id = '{event.user_id}' ''').fetchall())[2:-2]
            update_journal(event.user_id, a, 'monday')

        elif 'изменить вторник:' in request:
            a = request.replace('изменить вторник: ', '').split(', ')
            result = str(cur.execute(f'''SELECT group_id FROM users
                            WHERE user_id = '{event.user_id}' ''').fetchall())[2:-2]
            update_journal(event.user_id, a, 'tuesday')
        elif 'изменить среду:' in request:
            a = request.replace('изменить среду: ', '').split(', ')
            result = str(cur.execute(f'''SELECT group_id FROM users
                                   WHERE user_id = '{event.user_id}' ''').fetchall())[2:-2]
            update_journal(event.user_id, a, 'wednesday')

        elif 'изменить четверг:' in request:
            a = request.replace('изменить четверг: ', '').split(', ')
            result = str(cur.execute(f'''SELECT group_id FROM users
                                   WHERE user_id = '{event.user_id}' ''').fetchall())[2:-2]
            update_journal(event.user_id, a, 'thursday')

        elif 'изменить пятницу:' in request:
            a = request.replace('изменить пятницу: ', '').split(', ')
            result = str(cur.execute(f'''SELECT group_id FROM users
                                   WHERE user_id = '{event.user_id}' ''').fetchall())[2:-2]
            update_journal(event.user_id, a, 'friday')

        elif 'изменить субботу:' in request:
            b = f"""SELECT * FROM sqlite_master WHERE type = 'table' AND name = '{group_id}' AND sql LIKE '%saturday%'"""
            if b == '':
                write_msg(event.user_id, f'Ваше расписание работает по пятидневной системе обучения')
                continue
            a = request.replace('изменить субботу: ', '').split(', ')
            result = str(cur.execute(f'''SELECT group_id FROM users
                                   WHERE user_id = '{event.user_id}' ''').fetchall())[2:-2]
            update_journal(event.user_id, a, 'saturday')

        elif request == 'расписание понедельник':
            mess = ''
            group_id = get_group_id(event.user_id)
            print(group_id)
            rasp = cur.execute(f'''SELECT monday FROM {group_id} ''').fetchall()
            for j in rasp:
                print(j)
                if str(j)[2:-3] != 'on':
                    mess = mess + str(j)[2:-3] + '\n'
            if mess == '':
                write_msg(event.user_id, f'Не найдено рассписания на понедельник, возможно вы его не записали или удалили')
            else:
                write_msg(event.user_id, mess)

        elif request == 'расписание вторник':
            mess = ''
            group_id = get_group_id(event.user_id)
            print(group_id)
            rasp = cur.execute(f'''SELECT tuesday FROM {group_id} ''').fetchall()
            for j in rasp:
                print(j)
                if str(j)[2:-3] != 'on':
                    mess = mess + str(j)[2:-3] + '\n'
            if mess == '':
                write_msg(event.user_id, f'Не найдено рассписания на вторник, возможно вы его не записали или удалили')
            else:
                write_msg(event.user_id, mess)

        elif request == 'расписание среда':
            mess = ''
            group_id = get_group_id(event.user_id)
            print(group_id)
            rasp = cur.execute(f'''SELECT wednesday FROM {group_id} ''').fetchall()
            for j in rasp:
                print(j)
                if str(j)[2:-3] != 'on':
                    mess = mess + str(j)[2:-3] + '\n'
            if mess == '':
                write_msg(event.user_id, f'Не найдено рассписания на среду, возможно вы его не записали или удалили')
            else:
                write_msg(event.user_id, mess)

        elif request == 'расписание четверг':
            mess = ''
            group_id = get_group_id(event.user_id)
            print(group_id)
            rasp = cur.execute(f'''SELECT thursday FROM {group_id} ''').fetchall()
            for j in rasp:
                print(j)
                if str(j)[2:-3] != 'on':
                    mess = mess + str(j)[2:-3] + '\n'
            if mess == '':
                write_msg(event.user_id, f'Не найдено рассписания на четверг, возможно вы его не записали или удалили')
            else:
                write_msg(event.user_id, mess)

        elif request == 'расписание пятница':
            mess = ''
            group_id = get_group_id(event.user_id)
            print(group_id)
            rasp = cur.execute(f'''SELECT friday FROM {group_id} ''').fetchall()
            for j in rasp:
                print(j)
                if str(j)[2:-3] != 'on':
                    mess = mess + str(j)[2:-3] + '\n'
            if mess == '':
                write_msg(event.user_id, f'Не найдено рассписания на пятницу, возможно вы его не записали или удалили')
            else:
                write_msg(event.user_id, mess)

        elif request == 'расписание суббота':
            group_id = get_group_id(event.user_id)
            mess = ''
            a = f"""SELECT * FROM sqlite_master WHERE type = 'table' AND name = '{group_id}' AND sql LIKE '%saturday%'"""
            if a == '':
                write_msg(event.user_id, f'Ваше расписание работает по пятидневной системе обучения')
                continue
            print(group_id)
            rasp = cur.execute(f'''SELECT saturday FROM {group_id} ''').fetchall()
            for j in rasp:
                print(j)
                if str(j)[2:-3] != 'on':
                    mess = mess + str(j)[2:-3] + '\n'
            if mess == '':
                write_msg(event.user_id, f'Не найдено рассписания на субботу, возможно вы его не записали или удалили')
            else:
                write_msg(event.user_id, mess)


        elif request == 'расписание':
            mess = ''
            group_id = get_group_id(event.user_id)
            print(group_id)
            for i in days:
                rasp = cur.execute(f'''SELECT {i} FROM {group_id} ''').fetchall()
                for j in rasp:
                    print(j)
                    if str(j)[2:-3] != 'on':
                        mess = mess + str(j)[2:-3] + '\n'
                if mess == '':
                    write_msg(event.user_id, f'Не найдено рассписания на {i}, возможно вы его не записали или удалили')
                else:
                    write_msg(event.user_id, mess)
                mess = ''


        elif 'добавиться ' in request:
            write_msg(event.user_id, 'в процессе')
            a = request.replace('добавиться ', '').split(', ')
            group_id, password = a
            result = str(cur.execute(f"SELECT 1 FROM groups WHERE group_id = '{group_id}' AND password = '{password}' ").fetchall())[2:-3]
            print(result)
            if result == '1':
                cur.execute(f"UPDATE users SET group_id = '{group_id}' WHERE user_id = '{event.user_id}' ")
                con.commit()
                write_msg(event.user_id, f'Вы присоединены к классу {group_id}')

        else:
            write_msg(event.user_id, 'Бот еще пока на стадии разработки, но вы можете отправить своё мнение в гугл форму: https://docs.google.com/forms/d/e/1FAIpQLSdmE-1tzm7v40qQW0RKq4bLMjHWE2TuwGpAypjxfZ5lf4csGw/viewform?usp=sf_link')







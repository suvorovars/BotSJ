from vk_api import vk_api
from vk_api.longpoll import VkLongPoll

from sql_requests import *

vk_session = vk_api.VkApi(token="da3c917417e008d6f650f050a8b00c6ab0c4f84b3ff3f6a921890fe83445943508625a6e57c97b4f7c7cb")

longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

async def timetable(request, user_id):
    if request == 'расписание понедельник':
        mess = ''
        group_id = get_group_id(user_id)
        print(group_id)
        rasp = cur.execute(f'''SELECT monday FROM {group_id} ''').fetchall()
        for j in rasp:
            print(j)
            if str(j)[2:-3] != 'on':
                mess = mess + str(j)[2:-3] + '\n'
        if mess == '':
            asyncio.run(write_msg(user_id,
                                  f'Не найдено рассписания на понедельник, возможно вы его не записали или удалили'))
        else:
            asyncio.run(write_msg(user_id, mess))

    elif request == 'расписание вторник':
        mess = ''
        group_id = get_group_id(user_id)
        print(group_id)
        rasp = cur.execute(f'''SELECT tuesday FROM {group_id} ''').fetchall()
        for j in rasp:
            print(j)
            if str(j)[2:-3] != 'on':
                mess = mess + str(j)[2:-3] + '\n'
        if mess == '':
            asyncio.run(write_msg(user_id,
                                  f'Не найдено рассписания на вторник, возможно вы его не записали или удалили'))
        else:
            asyncio.run(write_msg(user_id, mess))

    elif request == 'расписание среда':
        mess = ''
        group_id = get_group_id(user_id)
        print(group_id)
        rasp = cur.execute(f'''SELECT wednesday FROM {group_id} ''').fetchall()
        for j in rasp:
            print(j)
            if str(j)[2:-3] != 'on':
                mess = mess + str(j)[2:-3] + '\n'
        if mess == '':
            asyncio.run(write_msg(user_id, f'Не найдено рассписания на среду, возможно вы его не записали или удалили'))
        else:
            asyncio.run(write_msg(user_id, mess))

    elif request == 'расписание четверг':
        mess = ''
        group_id = get_group_id(user_id)
        print(group_id)
        rasp = cur.execute(f'''SELECT thursday FROM {group_id} ''').fetchall()
        for j in rasp:
            print(j)
            if str(j)[2:-3] != 'on':
                mess = mess + str(j)[2:-3] + '\n'
        if mess == '':
            asyncio.run(write_msg(user_id,
                                  f'Не найдено рассписания на четверг, возможно вы его не записали или удалили'))
        else:
            asyncio.run(write_msg(user_id, mess))

    elif request == 'расписание пятница':
        mess = ''
        group_id = get_group_id(user_id)
        print(group_id)
        rasp = cur.execute(f'''SELECT friday FROM {group_id} ''').fetchall()
        for j in rasp:
            print(j)
            if str(j)[2:-3] != 'on':
                mess = mess + str(j)[2:-3] + '\n'
        if mess == '':
            asyncio.run(write_msg(user_id,
                                  f'Не найдено рассписания на пятницу, возможно вы его не записали или удалили'))
        else:
            asyncio.run(write_msg(user_id, mess))

    elif request == 'расписание суббота':
        group_id = get_group_id(user_id)
        mess = ''
        a = f"""SELECT * FROM sqlite_master WHERE type = 'table' AND name = '{group_id}' AND sql LIKE '%saturday%'"""
        if a == '':
            asyncio.run(write_msg(user_id, f'Ваше расписание работает по пятидневной системе обучения'))
            return None
        print(group_id)
        rasp = cur.execute(f'''SELECT saturday FROM {group_id} ''').fetchall()
        for j in rasp:
            print(j)
            if str(j)[2:-3] != 'on':
                mess = mess + str(j)[2:-3] + '\n'
        if mess == '':
            asyncio.run(write_msg(user_id,
                                  f'Не найдено рассписания на субботу, возможно вы его не записали или удалили'))
        else:
            asyncio.run(write_msg(user_id, mess))

    elif request == 'расписание':
        mess = ''
        group_id = get_group_id(user_id)
        print(group_id)
        for i in days:
            rasp = cur.execute(f'''SELECT {i} FROM {group_id} ''').fetchall()
            for j in rasp:
                print(j)
                if str(j)[2:-3] != 'on':
                    mess = mess + str(j)[2:-3] + '\n'
            if mess == '':
                asyncio.run(write_msg(user_id, f'Не найдено рассписания на {i}, возможно вы его не записали или удалили'))
            else:
                asyncio.run(write_msg(user_id, mess))
            mess = ''
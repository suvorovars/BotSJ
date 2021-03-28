import datetime
import sqlite3

con = sqlite3.connect("reminders.db")
cur = con.cursor()


def write_reminder(date1, time, txt, user):
    day, month, year = date1.split(',')
    main_date = datetime.date(year, month, day)
    hour, minute = time.split(':')
    main_time = datetime.time(hour, minute)
    if presence_of_day(main_date):
        if presence_of_time(main_date, main_time):
            if presence_of_user(main_date, user):
                a = str(cur.execute(f'''SELECT {user} WHERE time = {time}''').fetchall())[2:-3]
                return f"У вас уже есть напоминание '{a}' на заданный день"
            else:
                cur.execute(f"""ALTER TABLE {user} ADD COLUMN COLNew TEXT""")
                con.commit()
                cur.execute(f"""UPDATE {main_date} SET {user} = '{txt}' WHERE time = '{main_time}' """)
                con.commit()
                return ''
        else:
            if presence_of_user(main_date, user):
                cur.execute(f"""INSERT INTO {str(main_date)}(time, {user}) VALUES('{str(main_time)}', '{txt}')""")
                con.commit()
            else:
                cur.execute(f"""ALTER TABLE {user} ADD COLUMN COLNew TEXT""")
                con.commit()
                cur.execute(f"""INSERT INTO {str(main_date)}(time, {user}) VALUES('{str(main_time)}', '{txt}')""")
                con.commit()





def presence_of_day(main_date):
    result = str(cur.execute(f'''SELECT name FROM sqlite_master
    WHERE type = 'table' AND name = '{str(main_date)}' ''').fetchall())[2:-3]
    if result == main_date:
        return True
    return False

def presence_of_time(main_date, time):
    result = str(cur.execute(f'''SELECT time FROM {main_date} WHERE time = '{time}' ''').fetchall())[2:-3]
    if result == time:
        return True
    return False

def presence_of_user(main_date, user):
    result = str(cur.execute(f'''SELECT * FROM sqlite_master 
                    WHERE type = 'table' AND name = '{main_date}' AND sql LIKE '%{user}%' ''').fetchall())[2:-3]
    if result == '':
        return False
    return True
import sqlite3

con = sqlite3.connect("BotSJ.db")
cur = con.cursor()


def new_class(user_id, group_id, password):
    try:
        result = str(cur.execute(f'''SELECT group_id FROM groups
                        WHERE group_id = '{group_id}' ''').fetchall())[2:-3]
        print(result, '1')
        if result == '':
            cur.execute(f'''INSERT INTO groups(group_id, password) VALUES('{group_id}', '{password}') ''')
            con.commit()
            cur.execute(f'''UPDATE users SET group_id = '{group_id}' WHERE user_id = '{user_id}' ''')
            con.commit()
            cur.execute(f'''CREATE TABLE {group_id} (
            ID      INT,
            call    STRING,
            monday  STRING,
            tuesday STRING,
            wednesday STRING,
            thursday STRING,
            friday STRING); ''')
            con.commit()
            return True
        return False
    except:
        return False


def new_call(user_id, mess):
    group_id = str(cur.execute(f'''SELECT group_id FROM users
                        WHERE user_id = '{user_id}' ''').fetchall())[2:-3]
    result = str(cur.execute(f'''SELECT ID FROM {group_id}' ''').fetchall())[2:-3]
    if result == '':
        x = 1
        for i in mess:
            cur.execute(f'''INSERT INTO {group_id}(ID, call) VALUES({x}, {i}) ''')
            con.commit()
            x += 1


def user_presence(user_id):
    result = str(cur.execute(f'''SELECT user_id FROM users
        WHERE user_id = '{user_id}' ''').fetchall())[2:-3]
    if result != user_id:
        return False
    return True


def user_add(user_id):
    cur.execute(f'''INSERT INTO users(user_id, group_id) VALUES({user_id}, 'new_user') ''')
    con.commit()
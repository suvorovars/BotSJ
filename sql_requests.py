import sqlite3

con = sqlite3.connect("BotSJ.db")
cur = con.cursor()


def new_class(user_id, group_id, password, sixday=False):
    try:
        result = str(cur.execute(f'''SELECT group_id FROM groups
                        WHERE group_id = '{group_id}' ''').fetchall())[2:-3]
        print(result, '1')
        if result == '':
            cur.execute(f'''INSERT INTO groups(group_id, password) VALUES('{group_id}', '{password}') ''')
            con.commit()
            cur.execute(f'''UPDATE users SET group_id = '{group_id}' WHERE user_id = '{user_id}' ''')
            con.commit()
            if sixday:
                cur.execute(f'''CREATE TABLE {group_id} (
                ID      INT,
                call    STRING,
                monday  STRING,
                tuesday STRING,
                wednesday STRING,
                thursday STRING,
                friday STRING,
                saturday STRING); ''')
            else:
                cur.execute(f'''CREATE TABLE {group_id} (
                ID      INT,
                call    STRING,
                monday  STRING,
                tuesday STRING,
                wednesday STRING,
                thursday STRING,
                friday STRING); ''')
            con.commit()
            for i in range(1, 11):
                cur.execute(f'''INSERT INTO {group_id}(ID) VALUES({i})''')
            con.commit()
            return True

        return False
    except:
        return False


def update_journal(user_id, mess, val_update):
    group_id = get_group_id(user_id)
    print(group_id)
    result = str(cur.execute(f'''SELECT ID FROM {group_id} ''').fetchall())[2:-3]
    print(result)
    if result != '':
        for i in range(len(mess)):
            print(mess[i])
            cur.execute(f'''UPDATE {group_id} SET {val_update} = '{mess[i]}' WHERE ID = {i + 1}''')
        con.commit()


def user_presence(user_id):
    result = str(cur.execute(f'''SELECT 1 FROM users
        WHERE user_id = '{user_id}' ''').fetchall())[2:-3]
    if result == '1':
        return False
    return True


def user_add(user_id):
    cur.execute(f'''INSERT INTO users(user_id, group_id) VALUES({user_id}, 'new_user') ''')
    con.commit()


def get_group_id(user_id):
    return str(cur.execute(f'''SELECT group_id FROM users WHERE user_id = '{user_id}' ''').fetchall())[2:-3]


import sqlite3


def create_table():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    author_id INTEGER NOT NULL);''')

    connection.commit()
    connection.close()


def insert(title, desc, author_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute(f'''
    INSERT INTO objects (title, description, author_id)
    VALUES("{title}", "{desc}", "{author_id}");''')
    qr_id = cursor.execute("SELECT last_insert_rowid()").fetchone()[0]
    connection.commit()
    connection.close()
    return qr_id


def get_by_id(qr_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    data = cursor.execute(f'''
    SELECT * FROM objects WHERE id = {qr_id};''').fetchone()
    data = {'title': data[1], 'desc': data[2], 'author_id': data[3]}
    connection.commit()
    connection.close()
    return data

def get_all_by_user_id(user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    data = cursor.execute(f'''
    SELECT * FROM objects WHERE author_id = {user_id};''').fetchall()

    result = []
    for item in data:
        result.append({'id': item[0], 'title': item[1], 'desc': item[2], 'author_id': item[3]})

    connection.commit()
    connection.close()
    return result

def delete_qr_by_id(qr_id, user_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    data = cursor.execute(f'''
    DELETE FROM objects WHERE id = {qr_id} and author_id = {user_id};''')
    connection.commit()
    connection.close()
    return data

create_table()
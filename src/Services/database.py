import sqlite3

def criar_table():
    conn = sqlite3.connect('projeto_integrador.db')
    query = """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created TIMESTAMP NOT NULL,
            name varchar(100) NOT NULL,
            email varchar(100) NOT NULL,
            phone varchar(100) NOT NULL,
            message varchar(1000) NOT NULL
        );
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()


def insert_message(name, email, phone, message):
    import datetime
    conn = sqlite3.connect('projeto_integrador.db')
    query = "insert into posts (created, name, email, phone, message) values (?, ?, ?, ?, ?);"
    cursor = conn.cursor()
    cursor.execute(query, (datetime.datetime.now(), name, email, phone, message))
    conn.commit()
    conn.close()

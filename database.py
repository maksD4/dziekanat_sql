import sqlite3

DB_NAME = "dziekanat.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def load_ddl_file(conn, file_name):
    cursor = conn.cursor()

    with open(file_name, 'r', encoding="utf=8") as f:
        ddl_script = f.read()

    cursor.executescript(ddl_script)

    conn.commit()
    conn.close()

def init_db():
    conn = get_conn()
    load_ddl_file(conn, 'dziekanat.ddl')
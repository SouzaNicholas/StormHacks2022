import sqlite3 as sql


def open_db() -> (sql.Connection, sql.Cursor):
    conn = sql.connect("logs.db")
    curs = conn.cursor()
    init_logs_table(curs)
    return conn, curs


def close_db(conn: sql.Connection):
    conn.commit()
    conn.close()


# All keywords have "log_" in front of them to differentiate
def init_logs_table(curs: sql.Cursor):
    curs.execute("""CREATE TABLE IF NOT EXISTS logs(
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    log_date TEXT NOT NULL,
                    emotion TEXT NOT NULL,
                    log_action TEXT,
                    cause TEXT
    );""")


def query_db(terms: dict):
    db = open_db()
    print(terms.values())
    # db[1].execute("""SELECT date, emotion, action, cause FROM logs WHERE
    #                     log_date LIKE (?) AND
    #                     emotion LIKE (?) AND
    #                     log_action LIKE (?) AND
    #                     cause LIKE (?)""", (terms.values()))
    close_db(db[0])

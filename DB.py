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


# The idea here is to use LIKE to find any instance of select terms entered by the user
# The commented out block was my original idea that is giving undocumented errors.
# the block after is my attempt to fix it, it is not currently coherent.
def query_db(terms: dict):
    db = open_db()
    # db[1].execute("""SELECT log_date, emotion, log_action, cause FROM logs WHERE
    #                     log_date LIKE (?) AND
    #                     emotion LIKE (?) AND
    #                     log_action LIKE (?) AND
    #                     cause LIKE (?)""", (terms.values()))
    r = db[1].execute("""SELECT log_date, emotion, log_action, cause FROM logs WHERE
                        log_date LIKE ('%' || ? || '%');""", "A")
    print(r.fetchall())
    close_db(db[0])

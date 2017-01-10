from .SQLiteAccess import get_db, query_db
import time


def add_connection(uid):
    cursor = get_db().cursor()
    cursor.execute("INSERT INTO Connections VALUES (?,?,?)", (uid, int(time.time()), True))
    get_db().commit()


def close_connection(uid):
    cursor = get_db().cursor()
    cursor.execute("UPDATE Connections SET is_online = ? WHERE id = ?", (False, uid))
    get_db().commit()


def get_current_connections():
    connections = query_db("SELECT * FROM Connections WHERE is_online=1")
    return connections

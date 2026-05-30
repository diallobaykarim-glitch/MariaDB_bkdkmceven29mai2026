import mariadb

def get_connection():
    return mariadb.connect(
        host="localhost",
        user="root",
        password="root123",
        database="orl_ia"
    )
import pymysql

def get_conn():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="rootpw",
        db="jobplus",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

import sqlite3
import os
import yaml


DB = "screenshotComments.db"
DB_FILE = os.path.abspath(os.path.join(os.getcwd(), DB))
TABLE = "screenshot_comment"


def init_db():
    if os.path.exists(DB_FILE):
        return

    connection = sqlite3.connect(DB)
    cursor = connection.cursor()

    cursor.execute(f"create table {TABLE} (id integer PRIMARY KEY AUTOINCREMENT, screenshot_path VARCHAR, comment_num integer, comment_num_x integer unsigned, comment_num_y integer unsigned, comment VARCHAR);")
    connection.commit()

    cursor.close()
    connection.close()

    print("Init DB done!")

init_db()

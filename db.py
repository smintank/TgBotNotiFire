import os
from typing import Dict, List
import sqlite3

import settings


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]):
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"DELETE FROM {table} WHERE id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализация БД"""
    with open('create_db.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()
    fill_table()


def check_db_exists():
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='person'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


def fill_table():
    with open('fill_db.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def _del_db():
    try:
        os.remove(os.path.join(f'{settings.DB_PATH}', f'{settings.DB_NAME}'))
    except FileExistsError:
        pass


if settings.DEL_DB:
    "Удаление текущей БД"
    _del_db()


conn = sqlite3.connect(os.path.join(f'{settings.DB_PATH}', f'{settings.DB_NAME}'))
cursor = conn.cursor()
check_db_exists()

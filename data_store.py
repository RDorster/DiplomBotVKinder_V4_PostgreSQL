import psycopg2
from config import *

connection = psycopg2.connect(host=host, user=user, password=password, database=db_name)
connection.autocommit = True
# DB = 'table_seen_users'


"""оптимизация"""
def sql(sqltext):
    with connection.cursor() as cursor:
        cursor.execute(
            sqltext
        )


"""создание таблиц в базу"""
# """таблица пользователей"""
# def create_table_users():
#     sql(
#         """CREATE TABLE IF NOT EXISTS users
#             (
#                 id serial,
#                 vk_id varchar(20) NOT NULL PRIMARY KEY,
#                 vk_link varchar(75)
#             );"""
#     )
#     print("(SQL) Таблица users = ok")


"""таблица просмотренных пользователей"""
def create_table_seen_users():
    sql(
        """CREATE TABLE IF NOT EXISTS seen_users
            (
            id serial,
            vk_id varchar(20) PRIMARY KEY
            );"""
    )
    print("(SQL) Таблица seen_users = ok")


"""создание таблицы в базу"""
def creating_database():
    # create_table_users()
    create_table_seen_users()


def check(vk_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT vk_id
            FROM seen_users WHERE vk_id=%s;""", (vk_id)
        )
        return cursor.fetchone()
        # print(f"(SQL) Выбрано: {vk_id}")


# """заполнение таблицы пользователей"""
# def insert_data_users(vk_id, vk_link):
#     sql(
#         f"""INSERT INTO users (vk_id, vk_link)
#         VALUES ('{vk_id}', '{vk_link}');"""
#     )
#     print(f"(SQL) Запись user: {vk_id}")


"""заполнение таблицы просмотренных пользователей"""
def insert_data_seen_users(vk_id, offset):
    sql(
        f"""INSERT INTO seen_users (vk_id) 
            VALUES ('{vk_id}')
            OFFSET '{offset}';"""
    )
    print(f"(SQL) Запись seen user: {vk_id}")


# """выборка из непросмотренных пользователей"""
# def select(offset):
#     with connection.cursor() as cursor:
#         cursor.execute(
#             f"""SELECT
#                 users.vk_id,
#                 seen_users.vk_id
#                     FROM users
#                     LEFT JOIN seen_users
#                     ON users.vk_id = seen_users.vk_id
#                     WHERE seen_users.vk_id IS NULL
#                     OFFSET '{offset}';"""
#         )
#         return cursor.fetchone()

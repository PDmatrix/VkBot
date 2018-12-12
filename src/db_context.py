from src import days_helper
from src import logger
import psycopg2
import os


def db_query(query):
    result = None
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(os.environ.get('DATABASE_LIBPQ'))
        cur = conn.cursor()
        cur.execute(query)
        try:
            result = cur.fetchall()
        except Exception:
            result = None
        try:
            conn.commit()
        except Exception:
            pass
    except psycopg2.ProgrammingError as e:
        logger.error(
            "Query Failed: {query}\nDatabase error: {exception}",
            query=query,
            exception=str(e))
        result = None
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()
        return result


'''
-------------------------------------------------------------------------------------------------
ФУНКЦИИ ДЛЯ РАСПИСАНИЯ
-------------------------------------------------------------------------------------------------
'''


def get_schedule_by_group_name_and_day(group_name, day):
    """Расписание по названию группы и по дню недели"""
    group_name = group_name.lower().title()
    if str(day).isdigit():
        return [
            pair[0] for pair in db_query(
                f'SELECT pair '
                f'FROM schedule '
                f'WHERE group_id = \'{get_group_id(group_name)}\' AND day = {day}'
            )
        ]
    else:
        return [
            pair[0] for pair in db_query(
                f'SELECT pair '
                f'FROM schedule '
                f'WHERE group_id = \'{get_group_id(group_name)}\' AND day = {days_helper.get_day_num(day)}'
            )
        ]


def get_schedule_by_group_id_and_day(group_id, day):
    """Расписание по ид группы и по дню недели"""
    if str(day).isdigit():
        return [
            pair[0] for pair in db_query(
                f'SELECT pair '
                f'FROM schedule '
                f'WHERE group_id = \'{group_id}\' AND day = {day}')
        ]
    else:
        return [
            pair[0] for pair in db_query(
                f'SELECT pair '
                f'FROM schedule '
                f'WHERE group_id = \'{group_id}\' AND day = {days_helper.get_day_num(day)}'
            )
        ]


'''
----------------------------------------------------------------------------------------------------
ФУНКЦИИ ДЛЯ ГРУПП
----------------------------------------------------------------------------------------------------
'''


def get_groups():
    """Список групп"""
    return [group[0] for group in db_query('SELECT name FROM groups')]


def get_group_id(group_name):
    """Ид группы по названию группы"""
    group_name = group_name.lower().title()
    return db_query(f'SELECT id '
                    f'FROM groups '
                    f'WHERE name = \'{group_name}\'')[0][0]


def get_group_course(group_name):
    """Курс группы по названию группы"""
    group_name = group_name.lower().title()
    return db_query(f'SELECT course_num '
                    f'FROM groups '
                    f'WHERE name = \'{group_name}\'')[0][0]


def get_group_name(group_id):
    """Название группы по ид группы"""
    return db_query(f'SELECT name '
                    f'FROM groups '
                    f'WHERE id = {group_id}')[0][0]


def get_group_name_by_user_id(user_id):
    """Группа по ид юзера"""
    return get_group_name(
        db_query(f'SELECT group_id '
                 f'FROM users '
                 f'WHERE id = {user_id}')[0][0])


def get_ids_by_group_and_timer(group_name, timer=1):
    """Список пользователей у которых установлен таймер по группе"""
    group_name = group_name.lower().title()
    return [
        ids[0] for ids in db_query(
            f'SELECT id '
            f'FROM users '
            f'WHERE group_id = {get_group_id(group_name)} AND Timer = {timer}')
    ]


'''
-------------------------------------------------------------------------------------------------
ФУНКЦИИ ДЛЯ ПОЛЬЗОВАТЕЛЯ В ГЛАВНОЙ ТАБЛИЦЕ
-----------------------------------------------------------------------------------------------
'''


def is_user_exist(user_id):
    """Существует ли пользователь в главной таблице"""
    return db_query(f'SELECT id FROM users WHERE id = {user_id}') != []


def create_user(user_id, group_name='Пр1-15', timer=1):
    """Создать пользователя в главной таблице"""
    db_query(f'INSERT INTO users '
             f'VALUES({user_id}, {get_group_id(group_name)}, {timer})')


def delete_user(user_id):
    """Удалить пользователя в главной таблице"""
    db_query(f'DELETE FROM users WHERE id = {user_id}')


def get_users_with_timer():
    """Пользователи с таймером"""
    return [
        user[0] for user in db_query('SELECT id '
                                     'FROM users '
                                     'WHERE timer = 1')
    ]


def get_all_users():
    """Все пользователи"""
    return [user[0] for user in db_query('SELECT id FROM users')]


'''
-------------------------------------------------------------------------------------------------------
ФУНКЦИИ ДЛЯ РАБОТЫ С ТАЙМЕРОМ
-------------------------------------------------------------------------------------------------------
'''


def get_users_temp_timer(user_id):
    """Получить таймер пользователя из временной таблицы"""
    return db_query(f'SELECT timer '
                    f'FROM users_temp '
                    f'WHERE id = {user_id}')[0][0]


def get_users_timer(user_id):
    """Получить таймер пользователя из основной таблицы"""
    return db_query(f'SELECT timer '
                    f'FROM users '
                    f'WHERE id = {user_id}')[0][0]


def set_timer_to_user(user_id):
    """Установить таймер у пользователя"""
    db_query(f'UPDATE users SET timer = 1 WHERE id = {user_id}')


def unset_timer_to_user(user_id):
    """Убрать таймер у пользователя"""
    db_query(f'UPDATE users SET timer = 0 WHERE id = {user_id}')


'''
--------------------------------------------------------------------------------------------------------
ФУНКЦИИ ДЛЯ ПОЛЬЗОВАТЕЛЯ ВО ВРЕМЕННОЙ ТАБЛИЦЕ
---------------------------------------------------------------------------------------------------------
'''


def is_user_exist_temp(user_id):
    """Существует ли пользователь во временной таблице"""
    return db_query(f'SELECT id '
                    f'FROM users_temp '
                    f'WHERE id = {user_id}') != []


def delete_user_temp(user_id):
    """Удалить пользователя во временной таблице"""
    db_query(f'DELETE FROM users_temp WHERE id = {user_id}')


def create_user_temp(user_id, timer=1):
    """Создать пользователя во временной таблице"""
    db_query(f'INSERT INTO users_temp VALUES({user_id}, {0}, {timer})')

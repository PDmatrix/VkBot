from datetime import datetime
from src import days_helper
from src import db_context


def get_num(day):
    day = day.lower()
    if day.find("понедельник") != -1:
        return 0
    elif day.find("вторник") != -1:
        return 1
    elif day.find("среда") != -1:
        return 2
    elif day.find("четверг") != -1:
        return 3
    elif day.find("пятница") != -1:
        return 4
    elif day.find("суббота") != -1:
        return 5
    else:
        return "Неправильно введён день."


def get_schedule(group='Пр1-15', day="завтра"):
    date = datetime.today()
    week = date.weekday()
    day = day.lower()
    dc = {"пн": 0, "вт": 1, "ср": 2, "чт": 3, "пт": 4, "сб": 5}
    if day in dc.keys():
        week = dc[day]
    elif day == "сегодня":
        week = date.weekday()
        if week == 6:
            week = 5
    elif day == "завтра":
        week += 1
        if week >= 6:
            week = 0
    else:
        return "Введен неправильный день. " \
            "Возможные варианты: пн, вт, ср, чт, пт, сб, сегодня, завтра.",''
    return_value = days_helper.get_day_name(week) + '\n'
    for row in db_context.get_schedule_by_group_name_and_day(group, week):
        return_value += row + '\n'
    return return_value

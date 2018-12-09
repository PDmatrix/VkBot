from datetime import datetime
from src import command_system
from src import db_context


def fill_bell(group_name, course):
    message = ''
    if course == 1:
        if group_name in [
                "Ир1-18", "Ир3-18", "Ип1-18", "А1-18", "А3-18", "Бм1-18"
        ]:
            message += "2 пара:\n10:05–10:35\n10:55-11:55\n"
        elif group_name in [
                "Ип3-18", "Зи1-18", "Зи3-18", "Бм3-18", "Ки1-18", "Кс1-18"
        ]:
            message += "2 пара:\n10:05–10:50\n11:10-11:55\n"
        elif group_name in [
                "Ир5-18", "Ип5-18", "Т1-18", "Т3-18", "Кс3-18", "Кс5-18",
                "С1-18", "С3-18"
        ]:
            message += "2 пара:\n10:05–11:05\n11:25-11:55\n"
    elif course == 2:
        message += "2 пара:\n10:05–10:50\n10:55-11:40\n"
    else:
        message += "2 пара:\n10:25–11:55\n"
    return message


def bells(user_id):
    date = datetime.today()
    week = date.weekday()
    group_name = db_context.get_group_name_by_user_id(user_id)
    course = db_context.get_group_course(group_name)
    message = "1 пара:\n8:15 - 9:00\n9:10 – 9:55\n"
    class_hour = "Классный час:\n12:05 – 12:50\n"
    if week == 1:
        same = "4 пара:\n14:50 – 15:35\n15:45 – 16:30\n" \
                "5 пара:\n16:40 – 17:25\n17:30 – 18:15\n" \
                "6 пара:\n18:25 – 19:10\n19:15 – 20:00"
        message += fill_bell(group_name, course)
        message += class_hour
        if course == 1 or course == 2:
            message += "3 пара:\n13:00 – 13:45\n13:55 – 14:40\n"
        else:
            message += "3 пара:\n13:00–14:30\n"
        message += same
    else:
        same = "4 пара:\n14:00 – 14:45\n14:50 – 15:35\n" \
                "5 пара:\n15:45 – 16:30\n16:35 – 17:20\n" \
                "6 пара:\n17:30 – 18:15\n18:20 – 19:05"
        message += fill_bell(group_name, course)
        if course == 1 or course == 2:
            message += "3 пара:\n12:05 – 12:50\n12:55 – 13:40\n"
        else:
            message += "3 пара:\n12:05–13:35\n"
        message += same
    return message


info_command = command_system.Command()

info_command.keys = ['звонки', 'zvonki', 'Звонки на сегодня']
info_command.description = 'Звонки на сегодня'
info_command.process = bells
info_command.index = 3

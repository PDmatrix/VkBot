from src.commands.functions import schedule
from src import command_system
from src import db_context


def execute(user_id):
    return schedule.get_schedule(
        group=db_context.get_group_name_by_user_id(user_id), day='сегодня')


schedule_command = command_system.Command()

schedule_command.keys = [
    'расписание сегодня', 'sch today', 'schedule today', 'sch сегодня',
    'schedule сегодня', 'Расписание без замен на сегодня'
]
schedule_command.description = 'Расписание без замен на сегодня'
schedule_command.process = execute
schedule_command.index = 11

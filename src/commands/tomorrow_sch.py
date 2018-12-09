from src.commands.functions import schedule
from src import command_system
from src import db_context


def execute(user_id):
    return schedule.get_schedule(
        group=db_context.get_group_name_by_user_id(user_id))


schedule_command = command_system.Command()

schedule_command.keys = [
    'расписание', 'sch', 'schedule', 'расписание завтра', 'sch tomorrow',
    'schedule tomorrow', 'sch завтра', 'schedule завтра',
    'Расписание без замен на завтра'
]
schedule_command.description = 'Расписание без замен на завтра'
schedule_command.process = execute
schedule_command.index = 8

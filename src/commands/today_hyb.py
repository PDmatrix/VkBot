from src.commands.functions import hybrid
from src import command_system
from src import db_context


def execute(user_id):
    return hybrid.get_hybrid(
        group=db_context.get_group_name_by_user_id(user_id), day='сегодня')


rep_command = command_system.Command()
rep_command.keys = [
    'сегодня', 'гибрид сегодня', 'hyb today', 'hybrid today',
    'Расписание с заменами на сегодня'
]
rep_command.description = 'Расписание с заменами на сегодня'
rep_command.process = execute
rep_command.index = 7

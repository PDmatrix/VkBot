from src.commands.functions import hybrid
from src import command_system
from src import db_context


def execute(user_id):
    return hybrid.get_hybrid(
        group=db_context.get_group_name_by_user_id(user_id))


rep_command = command_system.Command()
rep_command.keys = [
    'завтра', 'гибрид завтра', 'hyb tomorrow', 'hybrid tomorrow',
    'Расписание с заменами на завтра'
]
rep_command.description = 'Расписание с заменами на завтра'
rep_command.process = execute
rep_command.index = 5

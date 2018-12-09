from src.commands.functions import replacements
from src import command_system
from src import db_context


def execute(user_id):
    return replacements.get_change(
        group=db_context.get_group_name_by_user_id(user_id), day='сегодня')


rep_command = command_system.Command()

rep_command.keys = [
    'замены сегодня', 'rep today', 'replacements today', 'rep сегодня',
    'replacements сегодня', 'Замены на сегодня'
]
rep_command.description = 'Замены на сегодня'
rep_command.process = execute
rep_command.index = 2

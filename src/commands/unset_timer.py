from src import command_system
from src import db_context


def unset_timer(user_id):
    db_context.unset_timer_to_user(user_id)
    return "Таймер убран!"


rep_command = command_system.Command()
rep_command.keys = ['убрать', 'убрать таймер', 'unset', 'unset timer']
rep_command.description = 'Убрать таймер'
rep_command.process = unset_timer
rep_command.index = 10
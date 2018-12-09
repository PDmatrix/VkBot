from src import command_system
from src import db_context


def set_timer(user_id):
    db_context.set_timer_to_user(user_id)
    return "Таймер установлен!"


rep_command = command_system.Command()
rep_command.keys = ['установить', 'установить таймер', 'set', 'set timer']
rep_command.description = 'Установить таймер'
rep_command.process = set_timer
rep_command.index = 4

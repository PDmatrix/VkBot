from src import command_system
from src import db_context


def about(user_id):
    return f"Группа: {db_context.get_group_name_by_user_id(user_id)}\n" \
           f"Таймер: {'Установлен' if db_context.get_users_timer(user_id) == 1 else 'Не установлен'}"


info_command = command_system.Command()

info_command.keys = ['информация', 'Информация', 'about']
info_command.description = 'Информация про пользователя'
info_command.process = about
info_command.index = 1

from src import command_system
from src import db_context


def change_group(user_id):
    timer = db_context.get_users_timer(user_id)
    db_context.delete_user(user_id)
    db_context.create_user_temp(user_id, timer)
    return f"Пожалуйста, введите свою группу.\nСписок групп:\n{', '.join(db_context.get_groups())}"


rep_command = command_system.Command()
rep_command.keys = ['сменить', 'сменить группу', 'change', 'change group']
rep_command.description = 'Сменить группу'
rep_command.index = 12
rep_command.process = change_group

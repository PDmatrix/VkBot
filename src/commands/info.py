from src import command_system


def info(user_id):
    message = []
    for c in command_system.command_list:
        message.append(f"{c.index}) {c.keys[0]} - {c.description}")
    return "\n".join(sorted(message, key=lambda x: int(x.split(")")[0])))


info_command = command_system.Command()

info_command.keys = ['помощь', 'помоги', 'help']
info_command.description = 'Список команд'
info_command.process = info
info_command.index = 6

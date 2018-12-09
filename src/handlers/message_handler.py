from src import vkapi
from src import command_system
from src import db_context
import json
import re
import os
import sys
import importlib


def _adjust_chat_message(message: str):
    return re.sub(r'^([\s\S])*(\]\s+|\],\s+)', '', message)


def _damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(d[(i - 1, j)] + 1, d[(i, j - 1)] + 1,
                            d[(i - 1, j - 1)] + cost)  # deletion
            # insertion
            # substitution
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)],
                                d[i - 2, j - 2] + cost)  # transposition
    return d[lenstr1 - 1, lenstr2 - 1]


def _load_modules():
    files = os.listdir('src/commands')
    modules = filter(lambda x: x.endswith('.py'), files)
    sys.path.insert(0, 'src/commands')
    for m in modules:
        importlib.import_module(m[0:-3])


def _get_answer(request_message, user_id):
    message = "Команда не распознана. Введите 'помощь', чтобы узнать команды"
    if request_message.isdigit():
        for c in command_system.command_list:
            if c.index == int(request_message):
                message = c.process(user_id)
        return message

    distance = len(request_message)
    command = None
    key = ''
    for _command in command_system.command_list:
        for _key in _command.keys:
            _distance = _damerau_levenshtein_distance(request_message, _key)
            if _distance < distance:
                distance = _distance
                command = _command
                key = _key
                if distance == 0:
                    message = _command.process(user_id)
                    return message
    if distance < len(request_message) * 0.4:
        message = command.process(user_id)
        message = f'Команда распознана как "{key}"\n\n{message}'
    return message


def handle_message(data):
    _load_modules()
    user_id = data['from_id']
    chat_id = data['peer_id']
    message = data['text']
    chat = False
    if user_id != chat_id:
        chat = True

    if not db_context.is_user_exist(user_id):
        if not db_context.is_user_exist_temp(user_id):
            vkapi.send_message_without_keyboard(
                user_id, f'Пожалуйста, введите свою группу.\n'
                f'Список групп:\n{", ".join(db_context.get_groups())}')
            db_context.create_user_temp(user_id)
            return
        elif message.lower().title() not in db_context.get_groups():
            vkapi.send_message_without_keyboard(
                user_id, f'Пожалуйста, введите свою группу.\n'
                f'Список групп:\n{", ".join(db_context.get_groups())}')
        else:
            vkapi.send_message_with_keyboard(
                user_id, f'Выбрана группа {message.lower().title()}.\n'
                f'Введите \'помощь\', чтобы узнать команды', "MainMenu")
            db_context.create_user(user_id, message,
                                   db_context.get_users_temp_timer(user_id))
            db_context.delete_user_temp(user_id)
            return 'User created'
    try:
        button = json.loads(data['payload'])['button']
    except Exception:
        button = None

    message = _get_answer(_adjust_chat_message(message.lower()), user_id)
    if chat:
        vkapi.send(chat_id, message)
    else:
        vkapi.send_message_with_keyboard(user_id, message, button)

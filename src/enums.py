import enum


class Replacements(enum.Enum):
    server_unavailable = "Сервер недоступен."
    something_wrong = "Что-то не так. Проверьте замены вручную."
    not_ready = "Расписание не готово."
    no_replacements = "Нет замен."

from src.handlers import auto_change_handler


def init_bot():
    auto_change_handler.register_scheduler()
    auto_change_handler.populate_groups()

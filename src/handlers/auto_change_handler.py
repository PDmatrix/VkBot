import threading
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src import db_context
from src.commands.functions import replacements
from src.enums import Replacements
import time
from src import logger
from src import vkapi


def _send_change(group: str, change: str):
    global groups_with_change
    ids_group = db_context.get_ids_by_group_and_timer(group)
    if ids_group:
        time.sleep(2)
        logger.info("Sending auto-change to {group}", group=group)
        vkapi.send_message_with_keyboard_to_many(
            ",".join(str(x) for x in ids_group), change, None)
    groups_with_change.update({group: change})


def _check_change():
    global groups_with_change
    groups = db_context.get_groups()
    for group in groups:
        change = replacements.get_change(group)
        if change != groups_with_change[group] and change != Replacements.server_unavailable.value \
                and change != Replacements.something_wrong.value \
                and change != Replacements.not_ready.value:
            _send_change(group, change)


def _populate():
    global groups_with_change
    for group in db_context.get_groups():
        groups_with_change.update({group: replacements.get_change(group)})


def register_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=_check_change,
        trigger=IntervalTrigger(seconds=60),
        id='CheckChange_job',
        name='Check new schedule',
        replace_existing=True)
    atexit.register(lambda: scheduler.shutdown())


def populate_groups():
    global groups_with_change
    groups_with_change = {}
    threading.Thread(target=_populate).start()

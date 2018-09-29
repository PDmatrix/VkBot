import requests
import datetime
import os
import threading


def _get_log_level(level):
    return {
        'verbose': "Verbose",
        'debug': "Debug",
        'info': "Information",
        'warning': "Warning",
        'error': "Error",
        'fatal': "Fatal"
    }.get(level, "Information")


def _log(message, level, **kwargs):
    server_url = os.environ.get("SEQ_SERVER_URL").rstrip('/')
    headers = {"X-Seq-ApiKey": os.environ.get("SEQ_API_KEY", "")}

    requests.post(f"{server_url}/api/events/raw?clef",
                  headers=headers,
                  json={'@t': datetime.datetime.utcnow().isoformat(), '@l': level,  '@mt': message, **kwargs})


def _run_thread(message, level, **kwargs):
    thr = threading.Thread(target=_log, args=(message, level,), kwargs={**kwargs})
    thr.start()


def verbose(message, **kwargs):
    _run_thread(message, _get_log_level("verbose"), **kwargs)


def debug(message, **kwargs):
    _run_thread(message, _get_log_level("debug"), **kwargs)


def info(message, **kwargs):
    _run_thread(message, _get_log_level("info"), **kwargs)


def warning(message, **kwargs):
    _run_thread(message, _get_log_level("warning"), **kwargs)


def error(message, **kwargs):
    _run_thread(message, _get_log_level("error"), **kwargs)


def fatal(message, **kwargs):
    _run_thread(message, _get_log_level("fatal"), **kwargs)
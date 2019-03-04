import requests
import datetime
import os


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
    server_url = os.environ.get("SEQ_SERVER_URL", None)
    if server_url is None:
        return

    server_url = server_url.rstrip("/")
    headers = {}

    api_key = os.environ.get("SEQ_API_KEY", None)
    if api_key is not None:
        headers.update({"X-Seq-ApiKey": api_key})

    authorization = os.environ.get("AUTHORIZATION_BASE64", None)
    if authorization is not None:
        headers.update({"Authorization": f"Basic {authorization}"})

    json = {
        '@t': datetime.datetime.utcnow().isoformat(),
        '@l': level,
        '@mt': message
    }

    exception = kwargs.pop('exception', None)
    if exception is not None:
        json['@x'] = exception

    json.update(**kwargs)

    requests.post(
        f"{server_url}/api/events/raw?clef", headers=headers, json=json)


def verbose(message, **kwargs):
    _log(message, _get_log_level("verbose"), **kwargs)


def debug(message, **kwargs):
    _log(message, _get_log_level("debug"), **kwargs)


def info(message, **kwargs):
    _log(message, _get_log_level("info"), **kwargs)


def warning(message, **kwargs):
    _log(message, _get_log_level("warning"), **kwargs)


def error(message, **kwargs):
    _log(message, _get_log_level("error"), **kwargs)


def fatal(message, **kwargs):
    _log(message, _get_log_level("fatal"), **kwargs)

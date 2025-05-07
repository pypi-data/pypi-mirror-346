from datetime import datetime


def get_date() -> str:
    return datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S+08:00")

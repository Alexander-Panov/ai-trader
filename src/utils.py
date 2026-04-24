from datetime import datetime

from config import MOSCOW_TZ


def now() -> datetime:
    return datetime.now(MOSCOW_TZ)


def format_datetime(date: datetime) -> str:
    return date.replace(second=0, minute=0, tzinfo=None).isoformat(timespec="seconds")


def now_str() -> str:
    return format_datetime(now())

from datetime import datetime, timedelta, timezone

from core.config import settings


def calculate_cache_expiration() -> int:
    """Calculates cahce expiration (in seconds) to reset time from project settings.

    Returns:
        int: Expiration in seconds
    """

    expiration_time = settings.cache.time_cache_expire_to

    dt_now = datetime.now(tz=timezone.utc)
    dt_reset = dt_now.replace(
        hour=expiration_time.hour,
        minute=expiration_time.minute,
        second=expiration_time.second,
        microsecond=expiration_time.microsecond,
    )

    if dt_now >= dt_reset:
        dt_reset += timedelta(days=1)

    return (dt_reset - dt_now).seconds

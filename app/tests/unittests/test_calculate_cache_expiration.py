from datetime import datetime, time, timezone
from unittest.mock import patch

from utils import calculate_cache_expiration


def test_calculate_cache_expiration():
    """Tests calculate_cache_expiration"""

    mock_expiration_time = time(hour=11)
    mock_now = datetime(2024, 1, 1, 10, tzinfo=timezone.utc)

    with (
        patch("utils.cache_expiration.settings") as mock_settings,
        patch("utils.cache_expiration.datetime") as mock_datetime,
    ):
        mock_settings.cache.time_cache_expire_to = mock_expiration_time
        mock_datetime.now.return_value = mock_now

        result = calculate_cache_expiration()

        mock_datetime.now.assert_called_once_with(tz=timezone.utc)

        assert result == 60 * 60

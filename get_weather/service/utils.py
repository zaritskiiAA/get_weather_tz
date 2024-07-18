from typing import Optional, Any
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests


def request(
        uri: str,
        query_params: Optional[dict[str, str]],
        request_data: Optional[dict[Any, Any]],
        method: str = 'GET',
        **kwargs,
) -> requests.Response:

    method = method.lower()

    if not request_data:
        request_data = {}

    if not query_params:
        query_params = {}

    if hasattr(requests, method):
        return getattr(requests, method)(
            uri, params=query_params, **request_data, **kwargs,
        )

    return requests.Response(
        {'method_not_allowed': 'Метод не обслуживается'},
        status=requests.status_codes.codes.NOT_ALLOWED,
    )


def seconds_to_date(seconds: int, format: str = '%Y-%m-%d') -> datetime:
    """
    Конвертирует количество секунд в объект datetime,
    представляющий дату и время.
    """
    epoch_start = datetime(1970, 1, 1, tzinfo=ZoneInfo('UTC'))
    result_time = epoch_start + timedelta(seconds=seconds)
    return result_time.strftime(format=format)

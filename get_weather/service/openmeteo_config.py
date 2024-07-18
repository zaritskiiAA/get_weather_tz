import openmeteo_requests
import requests_cache
from retry_requests import retry

from core.constants import (
    OPENMETEO_CASH_EXP, REQUEST_RETRIES, BACKOFF_FACTOR,
)


# https://open-meteo.com/en/docs#location_mode=csv_coordinates

cache_session = requests_cache.CachedSession(
    '.cache', expire_after=OPENMETEO_CASH_EXP,
)
retry_session = retry(
    cache_session, retries=REQUEST_RETRIES, backoff_factor=BACKOFF_FACTOR,
)
openmeteo = openmeteo_requests.Client(session=retry_session)

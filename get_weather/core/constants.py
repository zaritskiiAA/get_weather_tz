# Openmeteo
GEOCODING_URL = 'https://geocoding-api.open-meteo.com/v1/'
OPENMETEO_URL = "https://api.open-meteo.com/v1/"
FORECAST_PATH = 'forecast'
SEARCH_PATH = 'search'
OPENMETEO_CASH_EXP = 3600
REQUEST_RETRIES = 5
BACKOFF_FACTOR = 0.2
LANG = 'ru'
COUNT = 1
FORMAT = 'json'
DAY_FROM_SEC = 86400
FORECAST_HOURS = 12
FORECAST_PARAMS = {
    "current": "temperature_2m",
    "hourly": ["temperature_2m", "rain", "showers"],
    "daily": ["temperature_2m_max", "temperature_2m_min"],
}
GEOCODE_PARAMS = {
    'count': COUNT,
    'language': LANG,
    'format': FORMAT,
}
# Models
CITY_LENGTH = 150

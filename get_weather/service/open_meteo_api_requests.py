import os
import json
from collections import defaultdict
from io import BytesIO
from typing import Optional, Any

import pandas as pd
import requests
from openmeteo_requests import Client
from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse
from .openmeteo_config import openmeteo
from openmeteo_sdk.Variable import Variable
from openmeteo_sdk.VariableWithValues import VariableWithValues
from .utils import request, seconds_to_date


class OpenMeteoRequest:

    """
    Класс для отправки API запросов на openmeteo.
    Так как из коробки не все запросы поддежриваются,
    например на эндпоинт geocoding https://open-meteo.com/en/docs/geocoding-api,
    тогда используется метод get_geocode.
    """

    def get_forecast(
        self, url: str, path: str,
        query_params: Optional[dict[str, Any]],
        method: str = 'weather_api',
    ) -> list[WeatherApiResponse] | None:

        uri = self._generate_uri(url, path)
        method = method.lower()

        if not query_params:
            query_params = {}

        if self._is_allowed_method(openmeteo, method):
            return getattr(openmeteo, method)(uri, params=query_params)

    def get_weather_data(
        self, response: WeatherApiResponse,
        params: list[str] | None,
    ) -> dict[str, Any]:

        weather_data = {
            'current': int(self.current(response, params['current'])),
            'daily': self.daily(response, params['daily']),
            'hourly': self.hourly(response, params['hourly']),
        }
        return weather_data

    def hourly(
        self, response: WeatherApiResponse,
        hourly_params: list[str],
    ) -> dict[str, Any]:

        hourly = response.Hourly()
        hourly_time = range(hourly.Time(), hourly.TimeEnd(), hourly.Interval())
        horly_variables = list(map(
            lambda i: hourly.Variables(i), range(0, hourly.VariablesLength())
            )
        )

        hourly_data = defaultdict(list)
        for idx, time in enumerate(hourly_time):

            cur_hourly_data = []

            for var in horly_variables:
                if self._is_rain_or_shower(idx, var):
                    var = 'Да' if var.Values(idx) else 'Нет'
                else:
                    var = var.Values(idx)

                cur_hourly_data.append(var)

            hourly_data[seconds_to_date(time)].append(
                [seconds_to_date(time, '%H:%M')] + cur_hourly_data
            )
        return dict(hourly_data)

    @staticmethod
    def _is_rain_or_shower(idx: int, var: VariableWithValues) -> bool:

        return var.Variable() == Variable.rain or var.Variable() == Variable.showers

    @staticmethod
    def current(response: WeatherApiResponse, current_params: str) -> float:
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        return current_temperature_2m

    @staticmethod
    def daily(
        response: WeatherApiResponse, daily_params: list[str],
    ) -> pd.DataFrame:

        daily = response.Daily()
        daily_time = range(daily.Time(), daily.TimeEnd(), daily.Interval())
        daily_variables = list(map(
            lambda i: daily.Variables(i), range(0, daily.VariablesLength())
            )
        )

        daily_data = defaultdict(list)

        for idx, time in enumerate(daily_time):
            temperature = [var.Values(idx) for var in daily_variables]
            temperature.sort()
            daily_data[seconds_to_date(time)].extend(temperature)

        # django template не обрабатывает defaultdict
        return dict(daily_data)

    def get_geocode(
        self, url: str, path: str,
        query_params: dict[str, Any], method='GET',
    ) -> dict[str, Any] | None:

        response = self._get_geocode(url, path, query_params, method)
        if response:
            parse_data = self.parse_response(response.content)
            if 'results' in parse_data:
                results = parse_data['results'][0]
                geo_data = {
                    'name': results['name'],
                    'latitude': results['latitude'],
                    'longitude': results['longitude'],
                    'timezone': results['timezone'],
                }
                return geo_data

    def _get_geocode(
        self, url: str, path: str,
        query_params: dict[str, Any], method='GET',
    ) -> requests.Response | None:

        uri = self._generate_uri(url, path)
        response = request(uri, query_params, None, method=method)
        if response.status_code == 200:
            return response

    @staticmethod
    def _generate_uri(url, path):
        return os.path.join(url, path)

    @staticmethod
    def _is_allowed_method(client: Client, method: str) -> bool:

        return hasattr(client, method)

    def parse_response(self, response: BytesIO | list[dict[str, Any]]):

        # Api от openmeteo возвращают list[dict]
        if isinstance(response, list):
            return response[0]
        return json.loads(response)


requests_interface = OpenMeteoRequest()

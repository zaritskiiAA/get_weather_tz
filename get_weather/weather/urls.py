from django.urls import path

from .views import (
    GetWeatherView, WeatherResultView,
    DetailWeatherResultView, GetLastCityWeatherView, autocomplete,
)


urlpatterns = [
    path("get_weather/", GetWeatherView.as_view(), name='get_weather',),
    path(
        "get_weather/<str:name>", WeatherResultView.as_view(),
        name='weather_result',
    ),
    path(
        "detail_weather/<str:date>", DetailWeatherResultView.as_view(),
        name='detail_weather',
    ),
    path(
        "get_weather/last_query/", GetLastCityWeatherView.as_view(),
        name='last_query',
    ),
    path("autocomplete/", autocomplete, name='auto_complete',),
]

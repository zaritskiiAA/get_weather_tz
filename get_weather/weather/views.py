import logging
import json
import copy

from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from service.open_meteo_api_requests import requests_interface
from .forms import WeatherForm
from core.constants import (
    GEOCODING_URL, OPENMETEO_URL, FORECAST_PATH,
    SEARCH_PATH, GEOCODE_PARAMS, FORECAST_PARAMS,
)
from users.models import UserHistory, UserQuery

logger = logging.getLogger(__name__)


class GetWeatherView(LoginRequiredMixin, View):
    """Представление для запроса погоды."""

    form_class = WeatherForm
    template_name = 'weather/weather.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            return HttpResponseRedirect(
                reverse('weather_result', args=(city,)),
            )
        return render(request, self.template_name, {'form': form})


class GetLastCityWeatherView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        last_query = UserHistory.objects.get_last_user_query(request.user)
        if not last_query:
            logger.error('Пользователь запрашивает несуществующий ресурс')
            return HttpResponse('Вы не совершали ранее запросов', status=404)
        return HttpResponseRedirect(
            reverse('weather_result', args=(last_query.city,)),
        )


class WeatherResultView(LoginRequiredMixin, View):

    template_name = 'weather/weather_result.html'

    @transaction.atomic
    def get(self, request, *args, **kwargs):

        geocode_params = copy.copy(GEOCODE_PARAMS)
        geocode_params.update(kwargs)
        geocode = requests_interface.get_geocode(
            GEOCODING_URL, SEARCH_PATH, geocode_params,
        )
        if not geocode:
            logger.error('Не удалось получить гео-данные города')
            return HttpResponse(
                'Не удалось получить гео-данные города', status=400,
            )
        name = geocode.pop('name')
        query = UserQuery.objects.filter(
            city=name,
            latitude=geocode['latitude'],
            longitude=geocode['longitude'],
        )
        if not query.exists():
            query = UserQuery.objects.create(
                city=name,
                latitude=geocode['latitude'],
                longitude=geocode['longitude'],
            )
        else:
            query = query.first()
        UserHistory.objects.create(user=request.user, query=query)

        forecast_paramas = copy.deepcopy(FORECAST_PARAMS)
        forecast_paramas.update(geocode)
        forecast_responses = requests_interface.get_forecast(
            OPENMETEO_URL, FORECAST_PATH, forecast_paramas,
        )
        if not forecast_responses:
            logger.error('Не удалось получить данные о погоде')
            return HttpResponse(
                'Не удалось получить данные о погоде', status=400,
            )
        response = requests_interface.parse_response(forecast_responses)

        weather_data = requests_interface.get_weather_data(
            response, forecast_paramas,
        )
        weather_data['hourly'] = json.dumps(weather_data['hourly'])
        return render(request, self.template_name, context=weather_data)


class DetailWeatherResultView(LoginRequiredMixin, View):

    template_name = 'weather/weather_detail.html'

    def post(self, request, *args, **kwargs):
        date = kwargs.get('date')
        hourly = request.POST.get('hourly')
        decode_hourly = json.loads(hourly)
        return render(
            request, self.template_name,
            context={'hourly': decode_hourly[date]},
        )


def autocomplete(request):
    query = request.GET.get('term').capitalize()
    qs = UserQuery.objects.filter(city__icontains=query)

    result = [obj.city for obj in qs]
    return JsonResponse(result, safe=False)

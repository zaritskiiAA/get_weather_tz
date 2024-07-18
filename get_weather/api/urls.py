from django.urls import path

from .views import ListCityCountQueryView


urlpatterns = [
    path(
        'cities_query/', ListCityCountQueryView.as_view(), name='cities_query',
    ),
]

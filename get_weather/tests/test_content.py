from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.fixtures.user_factory import (
    UserFactory, UserQueryFactory, UserHistoryFactory,
)
from weather.forms import WeatherForm

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.user_query = UserQueryFactory()
        cls.history = UserHistoryFactory(user=cls.user)
        cls.get_weather_form = {
            'city': 'Moscow',
        }

    def test_get_weather_forms(self):

        url = reverse('get_weather')

        response = self.auth_client.get(url, data=self.get_weather_form)

        self.assertIsInstance(
            response.context['form'], WeatherForm,
            f'Форма для {url} не соответствует WeaherForm',
        )

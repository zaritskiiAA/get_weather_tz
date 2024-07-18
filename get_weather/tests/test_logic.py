from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.fixtures.user_factory import UserFactory
from users.models import UserQuery, UserHistory

User = get_user_model()


class TestLogic(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.get_weather_form = {
            'city': 'Moscow',
        }

    def test_user_can_get_weather(self):
        ru_var = {'Moscow': 'Москва'}
        url = reverse('get_weather')
        url_redirect = reverse(
            'weather_result',
            args=(self.get_weather_form['city'],),
        )
        response = self.auth_client.post(url, data=self.get_weather_form)
        self.assertRedirects(response, url_redirect)
        new_user_query = UserQuery.objects.get(
            city=ru_var[self.get_weather_form['city']],
        )
        new_user_history = UserHistory.objects.filter(
            user=self.user, query=new_user_query,
        )
        self.assertEqual(
            new_user_query.city, ru_var[self.get_weather_form['city']],
            msg=f'Убедитесь, что при запросе к {url_redirect} создается объект UserQuery', # noqa E501
        )
        self.assertTrue(
            new_user_history.exists(),
            msg=f'Убедитесь, что при запросе к {url_redirect} создается объект UserHistory', # noqa E501
        )

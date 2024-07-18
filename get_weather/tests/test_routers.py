from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.fixtures.user_factory import (
    UserFactory, UserQueryFactory, UserHistoryFactory,
)


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.user_query = UserQueryFactory()
        cls.history = UserHistoryFactory(user=cls.user)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('login')
        urls = (
            ('get_weather', None),
            ('weather_result', (self.user_query.city,)),
            ('detail_weather', (self.user_query.city,)),
        )
        for name, args in urls:
            with self.subTest(name=name, client=self.client):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_pages_availability_for_users(self):

        self.user_query.city = 'Москва'
        self.user_query.save()

        urls_optional_status_for_users = (
            (
                ('get_weather', None,), [(self.client, HTTPStatus.FOUND), (self.auth_client, HTTPStatus.OK)], # noqa E501
            ),
            (
                ('register', None,), [(self.client, HTTPStatus.OK),],
            ),
            (
                ('login', None,), [(self.client, HTTPStatus.OK),],
            ),
            (
                ('weather_result', (self.user_query.city,),), [(self.client, HTTPStatus.FOUND), (self.auth_client, HTTPStatus.OK)], # noqa E501
            ),
        )
        for urls, optional_status_for_users in urls_optional_status_for_users:
            name, args = urls
            for client_status in optional_status_for_users:
                client, status = client_status
                with self.subTest(client=client, name=name):
                    url = reverse(name, args=args)
                    response = client.get(url)
                    self.assertEqual(response.status_code, status)

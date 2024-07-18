import json

from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from tests.fixtures.user_factory import (
    UserFactory, UserQueryFactory, UserHistoryFactory,
)

User = get_user_model()


class TestApi(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.query_user = UserQueryFactory()
        cls.history = UserHistoryFactory(query=cls.query_user)

    def test_status_code(self):
        url = reverse('cities_query')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            f'Убедитесь, что запрос к  api {url} возвращает статус 200',
        )

    def test_content(self):
        url = reverse('cities_query')
        response = self.client.get(url)

        # factory.Faker возвращает Demical для координат.
        object_pattern = {
            'city': self.query_user.city,
            'latitude': float(self.query_user.latitude),
            'longitude': float(self.query_user.longitude),
            'query_count': 1,
        }
        parse_data = json.loads(response.content)
        self.assertTrue(
            len(parse_data),
            f'Убедитесь, что запрос к {url} возвращает данные',
        )
        self.assertDictEqual(parse_data[0], object_pattern)

    def test_create_query_count_logic(self):

        new_query = UserQueryFactory(city='Москва')
        retry_create_history = 3
        for _ in range(retry_create_history):
            UserHistoryFactory(query=new_query)

        url = reverse('cities_query')
        response = self.client.get(url)
        parse_data = [
            query for query in json.loads(response.content) if query['city'] == new_query.city # noqa E501
        ]
        self.assertEqual(retry_create_history, parse_data[0]['query_count'])

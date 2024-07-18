from rest_framework.generics import ListAPIView
from django.db.models import Count

from users.models import UserQuery
from .serializers import CityQuerySerializer


class ListCityCountQueryView(ListAPIView):
    """Представление API для запроса списка UserQuery."""

    serializer_class = CityQuerySerializer

    def get_queryset(self):
        qs = UserQuery.objects.all().annotate(
            query_count=Count('history__query'),
        )
        return qs

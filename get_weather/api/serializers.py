from rest_framework import serializers

from users.models import UserQuery


class CityQuerySerializer(serializers.ModelSerializer):
    """Сериализатор для обработки Query."""

    query_count = serializers.SerializerMethodField()

    class Meta:
        model = UserQuery
        fields = ('city', 'latitude', 'longitude', 'query_count')

    def get_query_count(self, obj):
        return obj.query_count

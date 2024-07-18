from django.db import models
from django.contrib.auth import get_user_model

from core.constants import CITY_LENGTH

User = get_user_model()


class UserQuery(models.Model):

    city = models.CharField(max_length=CITY_LENGTH)
    latitude = models.FloatField()
    longitude = models.FloatField()


class UserHistoryManager(models.Manager):

    def get_last_user_query(self, user):

        obj = self.model.objects.filter(user=user).select_related('query').last()
        if obj:
            return obj.query


class UserHistory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.ForeignKey(UserQuery, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    objects = UserHistoryManager()

    class Meta:
        default_related_name = 'history'

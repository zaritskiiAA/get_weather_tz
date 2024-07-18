from django import forms

from users.models import UserQuery


class WeatherForm(forms.ModelForm):
    """Форма для отправки запроса с погодой по названию города."""

    class Meta:
        model = UserQuery
        fields = ('city',)


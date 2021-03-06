from django import forms
from .models import *

employee = ["Михаил Розенберг", "Олег Буянов", "Евгений Маслов"]


class TaskFilter(forms.Form):
    employee_task = forms.CharField(
        label="Исполнитель",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    status_task = forms.CharField(
        label="Статус задачи",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    type_task = forms.CharField(
        label="Тип задачи",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    business_trip = forms.CharField(
        label="Отношение к командировке",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

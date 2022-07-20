from django import forms
from .models import *

employee = ["Михаил Розенберг", "Олег Буянов", "Евгений Маслов"]


class TaskFilter(forms.Form):
    employee_task = forms.CharField(label="Исполнитель", widget=forms.TextInput(attrs={"class": "form-control"}))
    status_task = forms.CharField(label="Статус задачи", widget=forms.TextInput(attrs={"class": "form-control"}))

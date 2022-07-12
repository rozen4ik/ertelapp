from django import forms
from .models import *


class TaskFilter(forms.Form):
    employee_task = forms.CharField(label="Исполнитель", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    status_task = forms.CharField(label="Статус задачи", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
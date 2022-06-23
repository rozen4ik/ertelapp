from django import forms
from .models import *


class TaskFilter(forms.Form):
    date_task = forms.DateField(label="Дата постановки", required=False, widget=forms.DateInput(attrs={"class":"form-control"}))
    employee_task = forms.CharField(label="Исполнитель", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
    status_task = forms.CharField(label="Статус задачи", required=False, widget=forms.TextInput(attrs={"class":"form-control"}))
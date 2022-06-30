import datetime

import requests
import xlwt
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.contrib.auth.models import User

from ertelapp import settings
from .forms import *
from .models import *
from task.models import Task


# Получение данных
def index(request):
    task = Task.objects.all().order_by("-id")
    users = User.objects.all().select_related('profile')
    form = TaskFilter(request.GET)
    if form.is_valid():
        if form.cleaned_data["date_task"]:
            task = task.filter(date_task=form.cleaned_data["date_task"])

        if form.cleaned_data["employee_task"]:
            task = task.filter(employee_task=form.cleaned_data["employee_task"])

        if form.cleaned_data["status_task"]:
            task = task.filter(status_task=form.cleaned_data["status_task"])

    return render(request, "task/tasks.html", {"task": task, "users": users, "form": form})


# Добавление данных
def create(request):
    if request.method == "POST":
        task = Task()
        init_task(request, task)

    return HttpResponseRedirect("/")


# Изменение данных
def edit(request, id):
    try:
        task = Task.objects.get(id=id)
        users = User.objects.all().select_related('profile')

        if request.method == "POST":
            init_task(request, task)
            return HttpResponseRedirect("/")
        else:
            return render(request, "task/edit.html", {"task": task, "users": users})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


# Удаление данных
def delete(request, id):
    try:
        person = Task.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


# Реализация экспорта данных в excel
def export_excel(request):
    response = HttpResponse(content_type='applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=report' + str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#',
               'Дата',
               'Время',
               'Задача',
               'Адрес выполнения',
               'Кто поручил',
               'Исполнитель',
               'Сроки выполнения',
               'Статус задачи']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = Task.objects.all().values_list('id', 'date_task', 'time_task', 'text_task', 'address_task', 'author_task',
                                          'employee_task', 'line_task', 'status_task')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


def init_task(request, task):
    task.date_task = request.POST.get("date_task")
    task.time_task = request.POST.get("time_task")
    task.text_task = request.POST.get("text_task")
    task.address_task = request.POST.get("address_task")
    task.author_task = request.user.first_name + " " + request.user.last_name
    task.employee_task = request.POST.get("employee_task")
    task.line_task = request.POST.get("line_task")
    task.status_task = request.POST.get("status_task")
    task.user_id = request.user.id
    task.save()

import datetime
import xlwt
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from ertelapp import settings
from .forms import *
from .models import *

filter_task = {}


# Получение данных
def index(request):
    task = Task.objects.all().order_by("-id")
    users = User.objects.all().select_related('profile')
    director_user = Profile.objects.get(position_dep_id_id=1)
    eng_user = Profile.objects.get(position_dep_id_id=7)
    sales_user = Profile.objects.get(position_dep_id_id=2)
    technical_user = Profile.objects.get(position_dep_id_id=3)
    engineering_task = Task.objects.filter(author_task=eng_user).order_by("-id")
    sales_task = Task.objects.filter(author_task=sales_user).order_by("-id")
    technical_task = Task.objects.filter(author_task=technical_user).order_by("-id")

    form = TaskFilter(request.GET)
    if form.is_valid():
        if form.cleaned_data["employee_task"]:
            task = task.filter(employee_task=form.cleaned_data["employee_task"])
        if form.cleaned_data["status_task"]:
            task = task.filter(status_task=form.cleaned_data["status_task"])

    global filter_task
    print(filter_task)
    filter_task = form.cleaned_data
    if filter_task:
        filter_employee = filter_task["employee_task"]
        filter_status = filter_task["status_task"]
        print(f"Поиск по {filter_employee} - {filter_status}")
    print(filter_task)

    end_task = Task.objects.all().latest("id")

    if request.user.username == director_user.user.username:
        if end_task is not None:
            end_task_fullname = end_task.employee_task.split()
            end_task_firstname = end_task_fullname[0]
            end_task_lastname = end_task_fullname[1]
            tg_chat_id = User.objects.get(first_name=end_task_firstname, last_name=end_task_lastname)
            tg_chat_id = Profile.objects.get(user_id=tg_chat_id).chat_id
            token_tg_bot = settings.TOKEN_TG_BOT
            return render(request, "task/tasks.html",
                          {"task": task, "users": users, "form": form, "end_task": end_task, "tg_chat_id": tg_chat_id,
                           "token_tg_bot": token_tg_bot})
        else:
            return render(request, "task/tasks.html", {"task": task, "users": users, "form": form})
    elif request.user.username == eng_user.user.username:
        if end_task is not None:
            end_task_fullname = end_task.employee_task.split()
            end_task_firstname = end_task_fullname[0]
            end_task_lastname = end_task_fullname[1]
            tg_chat_id = User.objects.get(first_name=end_task_firstname, last_name=end_task_lastname)
            tg_chat_id = Profile.objects.get(user_id=tg_chat_id).chat_id
            token_tg_bot = settings.TOKEN_TG_BOT
            return render(request, "task/role/engineering_task.html",
                          {"engineering_task": engineering_task, "users": users, "form": form,
                           "end_task": end_task, "tg_chat_id": tg_chat_id,
                           "token_tg_bot": token_tg_bot})
        else:
            return render(request, "task/role/engineering_task.html",
                          {"engineering_task": engineering_task, "users": users, "form": form})
    elif request.user.username == sales_user.user.username:
        if end_task is not None:
            end_task_fullname = end_task.employee_task.split()
            end_task_firstname = end_task_fullname[0]
            end_task_lastname = end_task_fullname[1]
            tg_chat_id = User.objects.get(first_name=end_task_firstname, last_name=end_task_lastname)
            tg_chat_id = Profile.objects.get(user_id=tg_chat_id).chat_id
            token_tg_bot = settings.TOKEN_TG_BOT
            return render(request, "task/role/sales_task.html",
                          {"sales_task": sales_task, "users": users, "form": form, "end_task": end_task,
                           "tg_chat_id": tg_chat_id,
                           "token_tg_bot": token_tg_bot})
        else:
            return render(request, "task/role/sales_task.html",
                          {"sales_task": sales_task, "users": users, "form": form})
    elif request.user.username == technical_user.user.username:
        if end_task is not None:
            end_task_fullname = end_task.employee_task.split()
            end_task_firstname = end_task_fullname[0]
            end_task_lastname = end_task_fullname[1]
            tg_chat_id = User.objects.get(first_name=end_task_firstname, last_name=end_task_lastname)
            tg_chat_id = Profile.objects.get(user_id=tg_chat_id).chat_id
            token_tg_bot = settings.TOKEN_TG_BOT
            return render(request, "task/role/technical_task.html",
                          {"technical_task": technical_task, "users": users, "form": form, "end_task": end_task,
                           "tg_chat_id": tg_chat_id,
                           "token_tg_bot": token_tg_bot})
        else:
            return render(request, "task/role/technical_task.html",
                          {"technical_task": technical_task, "users": users, "form": form})
    else:
        return render(request, "task/role/no_access.html")


# Вывод задачи по id
def index_detail(request, id):
    try:
        task = Task.objects.get(id=id)
        return render(request, "task/id_task.html", {"task": task})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


def index_bot(request):
    work_task = WorkTask.objects.all().order_by("-id")
    return render(request, "task/work_task.html", {"work_task": work_task})


def delete_work_task(request, id):
    try:
        work_task = WorkTask.objects.get(id=id)
        work_task.delete()
        return HttpResponseRedirect("/work_task/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


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
        task = Task.objects.get(id=id)
        task.delete()
        return HttpResponseRedirect("/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


# Реализация экспорта данных в excel таблицы Task
def export_excel_work_task(request):
    response = HttpResponse(content_type='applications/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=work_task' + str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['#',
               'Дата',
               'Время',
               'Исполнитель',
               'Местонахождение',
               'Номер задачи']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = WorkTask.objects.all().values_list('id', 'date_work_task', 'time_work_task', 'employee_work_task',
                                              'address_work_task', 'task_id')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


# Реализация экспорта данных в excel таблицы Task
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

    if filter_task:
        filter_employee = filter_task["employee_task"]
        filter_status = filter_task["status_task"]
        rows = Task.objects.filter(employee_task=filter_employee, status_task=filter_status).values_list('id',
                                                                                                         'date_task',
                                                                                                         'time_task',
                                                                                                         'text_task',
                                                                                                         'address_task',
                                                                                                         'author_task',
                                                                                                         'employee_task',
                                                                                                         'line_task',
                                                                                                         'status_task')
    else:
        rows = Task.objects.all().values_list('id', 'date_task', 'time_task', 'text_task', 'address_task',
                                              'author_task',
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

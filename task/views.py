import datetime

import xlwt
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import render

from counterparty.models import Counterparty
from .forms import *
from .models import Task, TypeWork
from .services.task_service import TaskService

# Словарь полей, по которым фильтруются данные таблицы Task
filter_task = dict
task_service = TaskService()


# Получение данных
def index(request):
    page_number = request.GET.get("page")
    task = task_service.get_objects_all(Task)
    type_work = task_service.get_objects_all(TypeWork)
    counterparty = task_service.get_objects_all(Counterparty)
    users = task_service.get_objects_all(User).select_related('profile')

    director_user = task_service.create_user_roles(1)
    eng_user = task_service.create_user_roles(7)
    sales_user = task_service.create_user_roles(2)
    technical_user = task_service.create_user_roles(3)
    accounting_user = task_service.create_user_roles(11)
    personnel_user = task_service.create_user_roles(13)
    storekeeper_user = task_service.create_user_roles(8)
    dispatcher_user = task_service.create_user_roles(10)
    director_tts_user = task_service.create_user_roles(15)
    manage_user = task_service.create_user_roles(4)

    engineering_task = Task.objects.filter(Q(author_task=eng_user) |
                                           Q(author_task=technical_user) |
                                           Q(author_task=dispatcher_user)).order_by("-id")
    sales_task = Task.objects.filter(author_task=sales_user).order_by("-id")
    technical_task = Task.objects.filter(Q(author_task=technical_user) |
                                         Q(author_task=eng_user) |
                                         Q(author_task=storekeeper_user) |
                                         Q(author_task=dispatcher_user)).order_by("-id")
    accounting_task = Task.objects.filter(author_task=accounting_user).order_by("-id")
    personnel_task = Task.objects.filter(author_task=personnel_user).order_by("-id")
    storekeeper_task = Task.objects.filter(Q(author_task=storekeeper_user) |
                                           Q(author_task=director_tts_user) |
                                           Q(author_task=dispatcher_user)).order_by("-id")
    dispatcher_task = Task.objects.filter(Q(author_task=technical_user) |
                                          Q(author_task=eng_user) |
                                          Q(author_task=storekeeper_user) |
                                          Q(author_task=dispatcher_user)).order_by("-id")
    director_tts_task = Task.objects.filter(author_task=director_tts_user).order_by("-id")
    manage_task = Task.objects.filter(author_task=manage_user).order_by("-id")

    form = TaskFilter(request.GET)
    if form.is_valid():
        if form.cleaned_data["employee_task"]:
            task = task.filter(employee_task=form.cleaned_data["employee_task"])
            engineering_task = engineering_task.filter(employee_task=form.cleaned_data["employee_task"])
            sales_task = sales_task.filter(employee_task=form.cleaned_data["employee_task"])
            technical_task = technical_task.filter(employee_task=form.cleaned_data["employee_task"])
            accounting_task = accounting_task.filter(employee_task=form.cleaned_data["employee_task"])
            personnel_task = personnel_task.filter(employee_task=form.cleaned_data["employee_task"])
            storekeeper_task = storekeeper_task.filter(employee_task=form.cleaned_data["employee_task"])
            dispatcher_task = dispatcher_task.filter(employee_task=form.cleaned_data["employee_task"])
            director_tts_task = director_tts_task.filter(employee_task=form.cleaned_data["employee_task"])
            manage_task = manage_task.filter(employee_task=form.cleaned_data["employee_task"])
        if form.cleaned_data["status_task"]:
            task = task.filter(status_task=form.cleaned_data["status_task"])
            engineering_task = engineering_task.filter(status_task=form.cleaned_data["status_task"])
            sales_task = sales_task.filter(status_task=form.cleaned_data["status_task"])
            technical_task = technical_task.filter(status_task=form.cleaned_data["status_task"])
            accounting_task = accounting_task.filter(status_task=form.cleaned_data["status_task"])
            personnel_task = personnel_task.filter(status_task=form.cleaned_data["status_task"])
            storekeeper_task = storekeeper_task.filter(status_task=form.cleaned_data["status_task"])
            dispatcher_task = dispatcher_task.filter(status_task=form.cleaned_data["status_task"])
            director_tts_task = director_tts_task.filter(status_task=form.cleaned_data["status_task"])
            manage_task = manage_task.filter(status_task=form.cleaned_data["status_task"])
        if form.cleaned_data["type_task"]:
            task = task.filter(type_task=form.cleaned_data["type_task"])
            engineering_task = engineering_task.filter(type_task=form.cleaned_data["type_task"])
            sales_task = sales_task.filter(type_task=form.cleaned_data["type_task"])
            technical_task = technical_task.filter(type_task=form.cleaned_data["type_task"])
            accounting_task = accounting_task.filter(type_task=form.cleaned_data["type_task"])
            personnel_task = personnel_task.filter(type_task=form.cleaned_data["type_task"])
            storekeeper_task = storekeeper_task.filter(type_task=form.cleaned_data["type_task"])
            dispatcher_task = dispatcher_task.filter(type_task=form.cleaned_data["type_task"])
            director_tts_task = director_tts_task.filter(type_task=form.cleaned_data["type_task"])
            manage_task = manage_task.filter(type_task=form.cleaned_data["type_task"])
        if form.cleaned_data["object_task"]:
            task = task.filter(object_task=form.cleaned_data["object_task"])
            engineering_task = engineering_task.filter(object_task=form.cleaned_data["object_task"])
            sales_task = sales_task.filter(object_task=form.cleaned_data["object_task"])
            technical_task = technical_task.filter(object_task=form.cleaned_data["object_task"])
            accounting_task = accounting_task.filter(object_task=form.cleaned_data["object_task"])
            personnel_task = personnel_task.filter(object_task=form.cleaned_data["object_task"])
            storekeeper_task = storekeeper_task.filter(object_task=form.cleaned_data["object_task"])
            dispatcher_task = dispatcher_task.filter(object_task=form.cleaned_data["object_task"])
            director_tts_task = director_tts_task.filter(object_task=form.cleaned_data["object_task"])
            manage_task = manage_task.filter(object_task=form.cleaned_data["object_task"])
        if form.cleaned_data["business_trip"]:
            task = task.filter(business_trip=form.cleaned_data["business_trip"])
            engineering_task = engineering_task.filter(business_trip=form.cleaned_data["business_trip"])
            sales_task = sales_task.filter(business_trip=form.cleaned_data["business_trip"])
            technical_task = technical_task.filter(business_trip=form.cleaned_data["business_trip"])
            accounting_task = accounting_task.filter(business_trip=form.cleaned_data["business_trip"])
            personnel_task = personnel_task.filter(business_trip=form.cleaned_data["business_trip"])
            storekeeper_task = storekeeper_task.filter(business_trip=form.cleaned_data["business_trip"])
            dispatcher_task = dispatcher_task.filter(business_trip=form.cleaned_data["business_trip"])
            director_tts_task = director_tts_task.filter(business_trip=form.cleaned_data["business_trip"])
            manage_task = manage_task.filter(business_trip=form.cleaned_data["business_trip"])
        if form.cleaned_data["start_date"] and form.cleaned_data["end_date"]:
            task = task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            engineering_task = engineering_task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            sales_task = sales_task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            technical_task = technical_task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            accounting_task = accounting_task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            personnel_task = personnel_task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            storekeeper_task = storekeeper_task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            dispatcher_task = dispatcher_task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            director_tts_task = director_tts_task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            manage_task = manage_task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))

    global filter_task
    filter_task = form.cleaned_data
    print(filter_task)

    dict_task = {
        "form": form,
        "counterparty": counterparty,
        "type_work": type_work
    }

    # Показ задач в зависимости от должности
    match request.user.username:
        case director_user.user.username:
            page_m = task_service.paginator(task, page_number)
            users = task_service.get_objects_all(User).select_related('profile')
            data_task = {
                "task": task,
                "page_m": page_m,
                "users": users,
            }
            data_task.update(dict_task)
            return render(request, "task/tasks.html", data_task)
        case eng_user.user.username:
            page_m = task_service.paginator(engineering_task, page_number)
            users = User.objects.filter(Q(profile__position_dep_id=3) | Q(profile__position_dep_id=5) |
                                        Q(profile__position_dep_id=6) | Q(profile__position_dep_id=7) |
                                        Q(profile__position_dep_id=10) | Q(profile__position_dep_id=12) |
                                        Q(profile__position_dep_id=16) | Q(profile__position_dep_id=8))
            data_task = {
                "engineering_task": engineering_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/engineering_task.html", data_task)
        case sales_user.user.username:
            page_m = task_service.paginator(sales_task, page_number)
            users = User.objects.filter(Q(profile__position_dep_id=2) | Q(profile__position_dep_id=4) |
                                        Q(profile__position_dep_id=8) | Q(profile__position_dep_id=9))
            data_task = {
                "sales_task": sales_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/sales_task.html", data_task)
        case technical_user.user.username:
            page_m = task_service.paginator(technical_task, page_number)
            users = User.objects.filter(Q(profile__position_dep_id=3) | Q(profile__position_dep_id=5) |
                                        Q(profile__position_dep_id=6) | Q(profile__position_dep_id=7) |
                                        Q(profile__position_dep_id=10) | Q(profile__position_dep_id=12) |
                                        Q(profile__position_dep_id=16) | Q(profile__position_dep_id=8))
            data_task = {
                "technical_task": technical_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/technical_task.html", data_task)
        case accounting_user.user.username:
            page_m = task_service.paginator(accounting_task, page_number)
            users = User.objects.all().select_related('profile')
            data_task = {
                "accounting_task": accounting_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/accounting_task.html", data_task)
        case personnel_user.user.username:
            page_m = task_service.paginator(personnel_task, page_number)
            users = User.objects.all().select_related('profile')
            data_task = {
                "personnel_task": personnel_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/personnel_task.html", data_task)
        case storekeeper_user.user.username:
            page_m = task_service.paginator(storekeeper_task, page_number)
            users = User.objects.all().select_related('profile')
            data_task = {
                "storekeeper_task": storekeeper_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/storekeeper_task.html", data_task)
        case dispatcher_user.user.username:
            page_m = task_service.paginator(dispatcher_task, page_number)
            users = User.objects.filter(Q(profile__position_dep_id=3) | Q(profile__position_dep_id=5) |
                                        Q(profile__position_dep_id=6) | Q(profile__position_dep_id=7) |
                                        Q(profile__position_dep_id=10) | Q(profile__position_dep_id=12) |
                                        Q(profile__position_dep_id=16) | Q(profile__position_dep_id=8))
            data_task = {
                "dispatcher_task": dispatcher_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/dispatcher_task.html", data_task)
        case director_tts_user.user.username:
            page_m = task_service.paginator(director_tts_task, page_number)
            users = User.objects.all().select_related('profile')
            data_task = {
                "director_tts_task": director_tts_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/director_tts_task.html", data_task)
        case manage_user.user.username:
            page_m = task_service.paginator(manage_task, page_number)
            users = User.objects.filter(Q(profile__position_dep_id=2) | Q(profile__position_dep_id=4) |
                                        Q(profile__position_dep_id=8) | Q(profile__position_dep_id=9))
            data_task = {
                "manage_task": manage_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/manage_task.html", data_task)
        case _:
            return render(request, "task/role/no_access.html")


# Добавление данных
def create(request):
    if request.method == "POST":
        task_service.create_task(request)
    return HttpResponseRedirect("/")


# Изменение данных
def edit(request, id):
    try:
        task = task_service.get_object_deatil(Task, id)
        users = task_service.get_objects_all(User).select_related('profile')
        counterparty = task_service.get_objects_all(Counterparty)
        type_work = task_service.get_objects_all(TypeWork)

        data = {
            "task": task,
            "users": users,
            "counterparty": counterparty,
            "type_work": type_work
        }

        if request.method == "POST":
            task_service.edit_task(request, task)
            return HttpResponseRedirect("/")
        else:
            return render(request, "task/edit.html", data)
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


# Реализация экспорта данных в excel таблицы Task
def export_excel(request):
    response = HttpResponse(content_type="applications/ms-excel")
    response["Content-Disposition"] = "attachment; filename=Task" + str(datetime.datetime.now()) + ".xls"

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("report")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "#",
        "Дата",
        "Время",
        "Задача",
        "Объект",
        "Адрес",
        "Кто поручил",
        "Исполнитель",
        "Приоритет",
        "Сроки выполнения",
        "Статус задачи",
        "Тип задачи",
        "Отношение к командировке",
        "Примечание",
        "Дата изменения"
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = task_service.find_filter_task(filter_task)
    rows = rows.order_by("-id")

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

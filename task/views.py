import datetime
import xlwt
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from counterparty.models import CounterpartyTO, CounterpartyWarrantyObligations
from .services.task_service import TaskService
from .forms import *
from .models import Task

# Словарь полей, по которым фильтруются данные таблицы Task
filter_task = dict
task_service = TaskService()


# Получение данных
def index(request):
    page_number = request.GET.get("page")
    task = task_service.get_objects_all(Task)
    counterparty_to = task_service.get_objects_all(CounterpartyTO)
    counterparty_warranty_obligations = task_service.get_objects_all(CounterpartyWarrantyObligations)
    users = task_service.get_objects_all(User).select_related('profile')

    director_user = task_service.create_user_roles(1)
    eng_user = task_service.create_user_roles(7)
    sales_user = task_service.create_user_roles(2)
    technical_user = task_service.create_user_roles(3)
    accounting_user = task_service.create_user_roles(11)
    personnel_user = task_service.create_user_roles(13)
    storekeeper_user = task_service.create_user_roles(8)

    engineering_task = Task.objects.filter(Q(author_task=eng_user) | Q(author_task=technical_user))
    sales_task = Task.objects.filter(author_task=sales_user)
    technical_task = Task.objects.filter(Q(author_task=technical_user) | Q(author_task=eng_user) |
                                         Q(author_task=storekeeper_user)).order_by("-id")
    accounting_task = Task.objects.filter(author_task=accounting_user).order_by("-id")
    personnel_task = Task.objects.filter(author_task=personnel_user).order_by("-id")
    storekeeper_task = Task.objects.filter(author_task=storekeeper_user).order_by("-id")

    form = TaskFilter(request.GET)
    if form.is_valid():
        if form.cleaned_data["employee_task"]:
            task = task.filter(employee_task=form.cleaned_data["employee_task"])
        if form.cleaned_data["status_task"]:
            task = task.filter(status_task=form.cleaned_data["status_task"])
        if form.cleaned_data["type_task"]:
            task = task.filter(type_task=form.cleaned_data["type_task"])
        if form.cleaned_data["business_trip"]:
            task = task.filter(business_trip=form.cleaned_data["business_trip"])

    global filter_task
    filter_task = form.cleaned_data

    dict_task = {
        "users": users,
        "form": form,
        "counterparty_to": counterparty_to,
        "counterparty_warranty_obligations": counterparty_warranty_obligations
    }

    # Показ задач в зависимости от должности
    match request.user.username:
        case director_user.user.username:
            page_m = task_service.paginator(task, page_number)
            first_dict_task = {
                "task": task,
                "page_m": page_m
            }
            first_dict_task.update(dict_task)
            return render(request, "task/tasks.html", first_dict_task)
        case eng_user.user.username:
            page_m = task_service.paginator(engineering_task, page_number)
            first_dict_task = {
                "engineering_task": engineering_task,
                "page_m": page_m
            }
            first_dict_task.update(dict_task)
            return render(request, "task/role/engineering_task.html", first_dict_task)
        case sales_user.user.username:
            page_m = task_service.paginator(sales_task, page_number)
            first_dict_task = {
                "sales_task": sales_task,
                "page_m": page_m
            }
            first_dict_task.update(dict_task)
            return render(request, "task/role/sales_task.html", first_dict_task)
        case technical_user.user.username:
            page_m = task_service.paginator(technical_task, page_number)
            first_dict_task = {
                "technical_task": technical_task,
                "page_m": page_m
            }
            first_dict_task.update(dict_task)
            return render(request, "task/role/technical_task.html", first_dict_task)
        case accounting_user.user.username:
            page_m = task_service.paginator(accounting_task, page_number)
            first_dict_task = {
                "accounting_task": accounting_task,
                "page_m": page_m
            }
            first_dict_task.update(dict_task)
            return render(request, "task/role/accounting_task.html", first_dict_task)
        case personnel_user.user.username:
            page_m = task_service.paginator(personnel_task, page_number)
            first_dict_task = {
                "personnel_task": personnel_task,
                "page_m": page_m
            }
            first_dict_task.update(dict_task)
            return render(request, "task/role/personnel_task.html", first_dict_task)
        case storekeeper_user.user.username:
            page_m = task_service.paginator(storekeeper_task, page_number)
            first_dict_task = {
                "storekeeper_task": storekeeper_task,
                "page_m": page_m
            }
            first_dict_task.update(dict_task)
            return render(request, "task/role/storekeeper_task.html", first_dict_task)
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
        counterparty_to = task_service.get_objects_all(CounterpartyTO)
        counterparty_warranty_obligations = task_service.get_objects_all(CounterpartyWarrantyObligations)

        data = {
            "task": task,
            "users": users,
            "counterparty_to": counterparty_to,
            "counterparty_warranty_obligations": counterparty_warranty_obligations
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

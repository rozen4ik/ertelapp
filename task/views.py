import datetime
import xlwt
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from ertelapp import settings
from .controllers.task_controller import TaskController
from .forms import *
from .models import *

# Словарь полей, по которым фильтруются данные таблицы Task
filter_task = {}

task_controller = TaskController()


# Формирование показа страницы в зависимости от отдела
def show_department_task(request, end_task, path_file, dict_task):
    if end_task is not None:
        end_task_fullname = end_task.employee_task.split()
        end_task_firstname = end_task_fullname[0]
        end_task_lastname = end_task_fullname[1]
        tg_chat_id = User.objects.get(first_name=end_task_firstname, last_name=end_task_lastname)
        tg_chat_id = Profile.objects.get(user_id=tg_chat_id).chat_id
        token_tg_bot = settings.TOKEN_TG_BOT
        dict_task["tg_chat_id"] = tg_chat_id
        dict_task["token_tg_bot"] = token_tg_bot
        return render(request, path_file, dict_task)
    else:
        return render(request, path_file, dict_task)


# Получение данных
def index(request):
    page_number = request.GET.get("page")
    task = task_controller.get_objects_all(Task)
    users = User.objects.all().select_related('profile')
    director_user = Profile.objects.get(position_dep_id_id=1)
    eng_user = Profile.objects.get(position_dep_id_id=7)
    sales_user = Profile.objects.get(position_dep_id_id=2)
    technical_user = Profile.objects.get(position_dep_id_id=3)
    accounting_user = Profile.objects.get(position_dep_id_id=11)
    personnel_user = Profile.objects.get(position_dep_id_id=13)
    engineering_task = Task.objects.filter(author_task=eng_user).order_by("-id")
    sales_task = Task.objects.filter(author_task=sales_user).order_by("-id")
    technical_task = Task.objects.filter(Q(author_task=technical_user) | Q(author_task=eng_user)).order_by("-id")
    accounting_task = Task.objects.filter(author_task=accounting_user).order_by("-id")
    personnel_task = Task.objects.filter(author_task=personnel_user).order_by("-id")
    counterparty_to = CounterpartyTO.objects.all()
    countrparty_warranty_obligations = CountrpartyWarrantyObligations.objects.all()

    form = TaskFilter(request.GET)
    if form.is_valid():
        if form.cleaned_data["employee_task"]:
            task = task.filter(employee_task=form.cleaned_data["employee_task"])
        if form.cleaned_data["status_task"]:
            task = task.filter(status_task=form.cleaned_data["status_task"])

    global filter_task
    filter_task = form.cleaned_data
    end_task = Task.objects.all().latest("id")

    dict_task = {
        "users": users,
        "form": form,
        "end_task": end_task,
        "counterparty_to": counterparty_to,
        "countrparty_warranty_obligations": countrparty_warranty_obligations
    }

    # Показ задач в зависимости от должности
    match request.user.username:
        case director_user.user.username:
            page_m = paginator(task, page_number)
            first_dict_task = {"task": task, "page_m": page_m}
            first_dict_task.update(dict_task)
            return show_department_task(request, end_task, "task/tasks.html", first_dict_task)
        case eng_user.user.username:
            page_m = paginator(engineering_task, page_number)
            first_dict_task = {"engineering_task": engineering_task, "page_m": page_m}
            first_dict_task.update(dict_task)
            return show_department_task(request, end_task, "task/role/engineering_task.html", first_dict_task)
        case sales_user.user.username:
            page_m = paginator(sales_task, page_number)
            first_dict_task = {"sales_task": sales_task, "page_m": page_m}
            first_dict_task.update(dict_task)
            return show_department_task(request, end_task, "task/role/sales_task.html", first_dict_task)
        case technical_user.user.username:
            page_m = paginator(technical_task, page_number)
            first_dict_task = {"technical_task": technical_task, "page_m": page_m}
            first_dict_task.update(dict_task)
            return show_department_task(request, end_task, "task/role/technical_task.html", first_dict_task)
        case accounting_user.user.username:
            page_m = paginator(accounting_task, page_number)
            first_dict_task = {"accounting_task": accounting_task, "page_m": page_m}
            return show_department_task(request, end_task, "task/role/accounting_task.html", first_dict_task)
        case personnel_user.user.username:
            page_m = paginator(personnel_task, page_number)
            first_dict_task = {"personnel_task": personnel_task, "page_m": page_m}
            return show_department_task(request, end_task, "task/role/personnel_task.html", first_dict_task)
        case _:
            return render(request, "task/role/no_access.html")


def paginator(model, number):
    page_model = Paginator(model, 10)
    return page_model.get_page(number)


# Добавление данных
def create(request):
    if request.method == "POST":
        task_controller.create_task(request)
    return HttpResponseRedirect("/")


# Изменение данных
def edit(request, id):
    try:
        task = task_controller.get_detail_object(Task, id)
        users = User.objects.all().select_related('profile')

        if request.method == "POST":
            task_controller.edit_task(request, task)
            return HttpResponseRedirect("/")
        else:
            return render(request, "task/edit.html", {"task": task, "users": users})
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


# # Удаление данных
# def delete(request, id):
#     try:
#         task = Task.objects.get(id=id)
#         task.delete()
#         return HttpResponseRedirect("/")
#     except Task.DoesNotExist:
#         return HttpResponseNotFound("<h2>Task not found</h2>")


# Вывод раздела контроль выполнения работ
def index_bot(request):
    work_task = task_controller.get_objects_all(WorkTask)
    return render(request, "task/work_task.html", {"work_task": work_task})


# Удаление записи в в разделе контроля выполнения работ
def delete_work_task(request, id):
    try:
        work_task = task_controller.get_detail_object(WorkTask, id)
        work_task.delete()
        return HttpResponseRedirect("/work_task/")
    except Task.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


def show_work_task_for_task(request, id):
    try:
        work_task_employee = WorkTask.objects.filter(task=id).order_by("-id")
        return render(request, "task/work_task_employee.html", {"work_task_employee": work_task_employee})
    except WorkTask.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")


def counterparty_to_detail(request, id):
    try:
        counterparty = task_controller.get_detail_object(CounterpartyTO, id)
        return render(request, "task/counterparty.html", {"counterparty": counterparty})
    except CounterpartyTO.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")


def countrparty_warranty_obligations_detail(request, id):
    try:
        counterparty = task_controller.get_detail_object(CountrpartyWarrantyObligations, id)
        return render(request, "task/counterparty.html", {"counterparty": counterparty})
    except CountrpartyWarrantyObligations.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")


# Реализация экспорта данных в excel таблицы WorkTask
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

    rows = rows.order_by("-id")

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

    rows = rows.order_by("-id")

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

import datetime
import xlwt
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import render

from work_task.models import WorkTask
from .forms import *
from .models import Task, TypeWork, BestEmployee
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
    manag_sales_user = task_service.create_user_roles(9)
    marketing_user = task_service.create_user_roles(18)

    engineering_task = Task.objects.filter(Q(author_task=eng_user) |
                                           Q(author_task=technical_user) |
                                           Q(author_task=dispatcher_user)).order_by("-id")
    sales_task = Task.objects.filter(Q(author_task=sales_user) |
                                     Q(author_task=manage_user) |
                                     Q(author_task=manag_sales_user)).order_by("-id")
    technical_task = Task.objects.filter(Q(author_task=technical_user) |
                                         Q(author_task=eng_user) |
                                         Q(author_task=storekeeper_user) |
                                         Q(author_task=dispatcher_user)).order_by("-id")
    accounting_task = Task.objects.filter(author_task=accounting_user).order_by("-id")
    personnel_task = Task.objects.filter(author_task=personnel_user).order_by("-id")
    storekeeper_task = Task.objects.filter(Q(author_task=storekeeper_user) |
                                           Q(author_task=director_tts_user) |
                                           Q(author_task=dispatcher_user) |
                                           Q(employee_task=storekeeper_user)).order_by("-id")
    dispatcher_task = Task.objects.filter(Q(author_task=technical_user) |
                                          Q(author_task=eng_user) |
                                          Q(author_task=storekeeper_user) |
                                          Q(author_task=dispatcher_user)).order_by("-id")
    director_tts_task = Task.objects.filter(author_task=director_tts_user).order_by("-id")
    manage_task = Task.objects.filter(Q(author_task=manage_user) |
                                      Q(author_task=sales_user) |
                                      Q(author_task=manag_sales_user)).order_by("-id")
    manag_sales_task = Task.objects.filter(Q(author_task=manag_sales_user) |
                                           Q(author_task=sales_user) |
                                           Q(author_task=manage_user)).order_by("-id")
    marketing_task = Task.objects.filter(Q(employee_task=marketing_user) |
                                         Q(author_task=marketing_user)).order_by("-id")


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
            manag_sales_task = manag_sales_task.filter(employee_task=form.cleaned_data["employee_task"])
            marketing_task = marketing_task.filter(employee_task=form.cleaned_data["employee_task"])
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
            manag_sales_task = manag_sales_task.filter(status_task=form.cleaned_data["status_task"])
            marketing_task = marketing_task.filter(status_task=form.cleaned_data["status_task"])
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
            manag_sales_task = manag_sales_task.filter(type_task=form.cleaned_data["type_task"])
            marketing_task = marketing_task.filter(type_task=form.cleaned_data["type_task"])
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
            manag_sales_task = manag_sales_task.filter(object_task=form.cleaned_data["object_task"])
            marketing_task = marketing_task.filter(object_task=form.cleaned_data["object_task"])
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
            manag_sales_task = manag_sales_task.filter(business_trip=form.cleaned_data["business_trip"])
            marketing_task = marketing_task.filter(business_trip=form.cleaned_data["business_trip"])
        if form.cleaned_data["start_date"] and form.cleaned_data["end_date"]:
            task = task.filter(date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            engineering_task = engineering_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            sales_task = sales_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            technical_task = technical_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            accounting_task = accounting_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            personnel_task = personnel_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            storekeeper_task = storekeeper_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            dispatcher_task = dispatcher_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            director_tts_task = director_tts_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            manage_task = manage_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            manag_sales_task = manag_sales_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))
            marketing_task = marketing_task.filter(
                date_task__range=(form.cleaned_data["start_date"], form.cleaned_data["end_date"]))

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
                                        Q(profile__position_dep_id=16) | Q(profile__position_dep_id=8) |
                                        Q(profile__position_dep_id=2) | Q(profile__position_dep_id=18))
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
                                        Q(profile__position_dep_id=8) | Q(profile__position_dep_id=9) |
                                        Q(profile__position_dep_id=7) | Q(profile__position_dep_id=3) |
                                        Q(profile__position_dep_id=18))
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
                                        Q(profile__position_dep_id=16) | Q(profile__position_dep_id=8) |
                                        Q(profile__position_dep_id=2) | Q(profile__position_dep_id=18))
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
                                        Q(profile__position_dep_id=16) | Q(profile__position_dep_id=8) |
                                        Q(profile__position_dep_id=2) | Q(profile__position_dep_id=18))
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
                                        Q(profile__position_dep_id=8) | Q(profile__position_dep_id=9) |
                                        Q(profile__position_dep_id=7) | Q(profile__position_dep_id=3) |
                                        Q(profile__position_dep_id=18))
            data_task = {
                "manage_task": manage_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/manage_task.html", data_task)
        case manag_sales_user.user.username:
            page_m = task_service.paginator(manag_sales_task, page_number)
            users = User.objects.filter(Q(profile__position_dep_id=2) | Q(profile__position_dep_id=4) |
                                        Q(profile__position_dep_id=8) | Q(profile__position_dep_id=9) |
                                        Q(profile__position_dep_id=7) | Q(profile__position_dep_id=3) |
                                        Q(profile__position_dep_id=18))

            data_task = {
                "manag_sales_task": manag_sales_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/manag_sales_task.html", data_task)
        case marketing_user.user.username:
            page_m = task_service.paginator(marketing_task, page_number)
            users = User.objects.filter(Q(profile__position_dep_id=7) | Q(profile__position_dep_id=2) |
                                        Q(profile__position_dep_id=3) | Q(profile__position_dep_id=8))

            data_task = {
                "marketing_task": marketing_task,
                "page_m": page_m,
                "users": users
            }
            data_task.update(dict_task)
            return render(request, "task/role/marketing_task.html", data_task)
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


filter_cont = dict


def reports(request):
    counterparty = Counterparty.objects.all()
    users = User.objects.all().select_related('profile')
    fo = ""
    global filter_cont

    reports_form = ReportsContFilter(request.GET)

    task_cont = Task.objects.all().order_by("-id")

    if reports_form.is_valid():
        if reports_form.cleaned_data["object_task"]:
            task_cont = Task.objects.filter(object_task=reports_form.cleaned_data["object_task"]).order_by("-id")

        filter_cont = reports_form.cleaned_data

        if filter_cont != {'object_task': ''}:
            fo = "yes"

        data = {
            "reports_form": reports_form,
            "counterparty": counterparty,
            "task_cont": task_cont,
            "users": users,
            "fo": fo
        }

        return render(request, "task/rep/counterparty.html", data)


filter_employee = dict


def rep_emp(request):
    rep_emp_form = ReportsEmployFilter(request.GET)
    work = WorkTask.objects.all()
    start_d = ""
    end_d = ""
    emp = ""
    fo = ""
    range_days = 0
    global filter_employee

    if rep_emp_form.is_valid():
        if rep_emp_form.cleaned_data["employee_task"]:
            emp = rep_emp_form.cleaned_data["employee_task"]
        if rep_emp_form.cleaned_data["start_date"] and rep_emp_form.cleaned_data["end_date"]:
            start_d = rep_emp_form.cleaned_data["start_date"]
            end_d = rep_emp_form.cleaned_data["end_date"]

            ed = f"{end_d:%j}"
            sd = f"{start_d:%j}"
            range_days = int(ed) - int(sd)

        filter_employee = rep_emp_form.cleaned_data
        print(filter_employee)

        start_time = ""
        end_time = ""
        ub_time = ""
        res_to_obj = ""
        res_on_obj = ""
        best_emp = BestEmployee.objects.all().delete()
        print("|   Дата   | Исполнитель  | Время до объекта | Время нахождения на объекте")
        for i in range(range_days):
            best_emp = BestEmployee()
            ms = f"{start_d}|{emp}|"
            best_emp.date_be = start_d
            best_emp.employee_be = emp
            work = work.filter(employee_work_task=emp)
            for w in work:
                if w.date_work_task == start_d:
                    if w.status_work_task == "Убыл на объект":
                        start_time = w.time_work_task
                    elif w.status_work_task == "Прибыл на объект":
                        end_time = w.time_work_task
                    elif w.status_work_task == "Убыл с объекта":
                        ub_time = w.time_work_task
                    if (start_time != "") and (end_time != ""):
                        res_to_obj = datetime.timedelta(
                            hours=int(str(end_time).split(":")[0]),
                            minutes=int(str(end_time).split(":")[1]),
                            seconds=int(str(end_time).split(":")[2])
                        ) - datetime.timedelta(
                            hours=int(str(start_time).split(":")[0]),
                            minutes=int(str(start_time).split(":")[1]),
                            seconds=int(str(start_time).split(":")[2])
                        )
                        if str(res_to_obj)[0] == "-":
                            temp_before = datetime.timedelta(
                                hours=24,
                                minutes=0,
                                seconds=0
                            ) - datetime.timedelta(
                                hours=int(str(start_time).split(":")[0]),
                                minutes=int(str(start_time).split(":")[1]),
                                seconds=int(str(start_time).split(":")[2])
                            )
                            temp_after = datetime.timedelta(
                                hours=0,
                                minutes=0,
                                seconds=0
                            ) + datetime.timedelta(
                                hours=int(str(end_time).split(":")[0]),
                                minutes=int(str(end_time).split(":")[1]),
                                seconds=int(str(end_time).split(":")[2])
                            )
                            res_to_obj = temp_before + temp_after
                        start_time = ""
                        ub_time = ""
                        ms += f"{res_to_obj}|"
                        best_emp.time_do_object = res_to_obj
                        res_to_obj = ""
                    elif (end_time != "") and (ub_time != ""):
                        res_on_obj = datetime.timedelta(
                            hours=int(str(ub_time).split(":")[0]),
                            minutes=int(str(ub_time).split(":")[1]),
                            seconds=int(str(ub_time).split(":")[2])
                        ) - datetime.timedelta(
                            hours=int(str(end_time).split(":")[0]),
                            minutes=int(str(end_time).split(":")[1]),
                            seconds=int(str(end_time).split(":")[2])
                        )
                        if str(res_on_obj)[0] == "-":
                            temp_before = datetime.timedelta(
                                hours=24,
                                minutes=0,
                                seconds=0
                            ) - datetime.timedelta(
                                hours=int(str(end_time).split(":")[0]),
                                minutes=int(str(end_time).split(":")[1]),
                                seconds=int(str(end_time).split(":")[2])
                            )
                            temp_after = datetime.timedelta(
                                hours=0,
                                minutes=0,
                                seconds=0
                            ) + datetime.timedelta(
                                hours=int(str(ub_time).split(":")[0]),
                                minutes=int(str(ub_time).split(":")[1]),
                                seconds=int(str(ub_time).split(":")[2])
                            )
                            res_on_obj = temp_before + temp_after
                        end_time = ""
                        ub_time = ""
                        if len(str(ms).split("|")) == 5:
                            r = str(ms).split("|")[3]
                            plus_time = datetime.timedelta(
                                hours=int(r.split(":")[0]),
                                minutes=int(r.split(":")[1]),
                                seconds=int(r.split(":")[2])
                            ) + res_on_obj
                            ms = str(ms).replace(r, str(plus_time))
                            best_emp.time_on_object = str(ms).split("|")[3]
                        else:
                            ms += f"{res_on_obj}|"
                            best_emp.time_on_object = res_on_obj
                            res_on_obj = ""

            best_emp.save()
            print(ms)
            ms = ""
            one_d = datetime.timedelta(1)
            start_d += one_d

        if filter_employee != {'employee_task': '', 'start_date': None, 'end_date': None}:
            fo = "yes"

        best_emp = BestEmployee.objects.all()
        full_time_to_obj = datetime.timedelta(hours=0, minutes=0, seconds=0)
        full_time_on_obj = datetime.timedelta(hours=0, minutes=0, seconds=0)

        for b in best_emp:
            full_time_to_obj += datetime.timedelta(
                hours=int(b.time_do_object.split(":")[0]),
                minutes=int(b.time_do_object.split(":")[1]),
                seconds=int(b.time_do_object.split(":")[2])
            )
            full_time_on_obj += datetime.timedelta(
                hours=int(b.time_on_object.split(":")[0]),
                minutes=int(b.time_on_object.split(":")[1]),
                seconds=int(b.time_on_object.split(":")[2])
            )

        full_time_to_obj = full_time_to_obj.total_seconds() / 3600
        full_time_on_obj = full_time_on_obj.total_seconds() / 3600

        best_emp = BestEmployee()
        best_emp.date_be = None
        best_emp.employee_be = "Всего:"
        best_emp.time_do_object = "%.2f" % full_time_to_obj
        best_emp.time_on_object = "%.2f" % full_time_on_obj
        best_emp.save()
        best_emp = BestEmployee.objects.all()
        data = {
            "rep_emp_form": rep_emp_form,
            "fo": fo,
            "best_emp": best_emp
        }

        return render(request, "task/rep/employee.html", data)


# Реализация экспорта данных в excel таблицы Task
def export_counterparty(request):
    response = HttpResponse(content_type="applications/ms-excel")
    response["Content-Disposition"] = "attachment; filename=Task" + str(datetime.datetime.now()) + ".xls"

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("report")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "#",
        "Контрагент",
        "Тип работ",
        "Задача",
        "Исполнитель",
        "Дата постановки задачи",
        "Дата окончания задачи",
        "Статус",
        "Комментарий"
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = task_service.find_reports_cont_filter(filter_cont)
    rows = rows.order_by("-id")
    print(rows)

    for row in rows:
        row_num += 1
        print(row)
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


def export_employee(request):
    response = HttpResponse(content_type="applications/ms-excel")
    response["Content-Disposition"] = "attachment; filename=Task" + str(datetime.datetime.now()) + ".xls"

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("report")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "Дата",
        "Исполнитель",
        "Время до объекта",
        "Время нахождения на объекте"
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = task_service.find_reports_employee_filter(filter_employee)

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

import requests
from django.contrib.auth.models import User
from counterparty.models import Counterparty
from employee.models import Profile
from ertelapp import settings
from service import Service
from task.models import *


class TaskService(Service):
    tg_chat_id: str
    token_tg_bot: str

    def create_user_roles(self, dep_id):
        result = Profile.objects.get(position_dep_id_id=dep_id)
        return result

    def task_layout(self, request, task):
        task.date_task = request.POST.get("date_task")
        task.time_task = request.POST.get("time_task")
        task.text_task = request.POST.get("text_task")
        task.object_task = request.POST.get("object_task")
        addr = Counterparty.objects.get(name=task.object_task.split("/")[0].strip())
        task.address_obj_task = addr.address
        task.author_task = request.user.first_name + " " + request.user.last_name
        task.employee_task = request.POST.get("employee_task")
        task.urgency_task = request.POST.get("urgency_task")
        task.line_task = request.POST.get("line_task")
        task.status_task = "Отдано в разработку"
        business_trip = request.POST.get("business_trip")
        if not business_trip:
            task.business_trip = "Не командировка"
        elif business_trip:
            task.business_trip = "Командировка"
        task.type_task = request.POST.get("type_task")
        task.save()

    def create_task(self, request):
        new_task = Task()
        self.task_layout(request, new_task)
        self.send_message_telegram(new_task, "У вас новая задача!")

    def edit_task(self, request, task):
        self.task_layout(request, task)
        self.send_message_telegram(task, f"Задача №{task.id} изменилась!")

    def send_message_telegram(self, task, msg):
        url = settings.URL_API
        em_pr = task.employee_task.split()
        user = User.objects.get(first_name=em_pr[0], last_name=em_pr[1])
        em_pr = Profile.objects.get(user=user)
        chat_id = em_pr.chat_id
        text = self.get_message(task)
        data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        requests.post(url, data={"chat_id": chat_id, "text": msg})
        requests.post(url, data=data)

    def find_reports_cont_filter(self, filter_task):
        field_filter = (
            filter_task["object_task"]
        )

        object_filter = field_filter

        if object_filter != "":
            rows = Task.objects.filter(
                object_task=object_filter
            )
        else:
            rows = Task.objects.all()

        return rows.values_list(
            "id",
            "object_task",
            "type_task",
            "text_task",
            "employee_task",
            "date_task",
            "line_task",
            "status_task",
            "note_task",
        )

    def find_reports_employee_filter(self, filter_task):
        field_filter = (
            filter_task["employee_task"],
            filter_task["start_date"],
            filter_task["end_date"]
        )

        employee_filter, start_filter, end_filter = field_filter

        if (employee_filter != "") and start_filter and end_filter:
            rows = BestEmployee.objects.all()

        return rows.values_list(
            "date_be",
            "employee_be",
            "time_do_object",
            "time_on_object",
        )

    def find_filter_task(self, filter_task):
        field_filter = (
            filter_task["employee_task"],
            filter_task["status_task"],
            filter_task["type_task"],
            filter_task["object_task"],
            filter_task["business_trip"],
            filter_task["start_date"],
            filter_task["end_date"]
        )

        employee_filter, status_filter, type_filter, object_filter, business_filter, start_date, end_date = field_filter

        if (employee_filter == "") and (status_filter == "") and (type_filter == "") and (object_filter == "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.all()
        elif (employee_filter != "") and (status_filter == "") and (type_filter == "") and (object_filter == "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter == "") and (object_filter == "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                status_task=status_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter != "") and (object_filter == "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                type_task=type_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter == "") and (object_filter != "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                object_task=object_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter == "") and (object_filter == "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                business_trip=business_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter == "") and (object_filter == "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter == "") and (object_filter == "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter != "") and (object_filter == "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                type_task=type_filter,
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter == "") and (object_filter != "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                object_task=object_filter
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter == "") and (object_filter == "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                business_trip=business_filter
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter == "") and (object_filter == "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                date_task__range=(start_date, end_date),
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter != "") and (object_filter == "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                status_task=status_filter,
                type_task=type_filter
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter == "") and (object_filter != "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                status_task=status_filter,
                object_task=object_filter
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter == "") and (object_filter == "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                status_task=status_filter,
                business_trip=business_filter
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter == "") and (object_filter == "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                status_task=status_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter != "") and (object_filter != "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                type_task=type_filter,
                object_task=object_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter != "") and (object_filter == "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                type_task=type_filter,
                business_trip=business_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter != "") and (object_filter == "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                type_task=type_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter == "") and (object_filter == "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                business_trip=business_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter == "") and (object_filter != "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                business_trip=business_filter,
                object_task=object_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter == "") and (object_filter != "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                object_task=object_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter != "") and (object_filter == "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                type_task=type_filter,
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter == "") and (object_filter != "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                object_task=object_filter,
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter == "") and (business_filter != "") and \
                (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                business_trip=business_filter
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter == "") and (object_filter == "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                date_task__range=(start_date, end_date),
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter != "") and (object_filter != "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                type_task=type_filter,
                object_task=object_filter
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter != "") and (object_filter == "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                type_task=type_filter,
                business_trip=business_filter
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter != "") and (object_filter == "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                type_task=type_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter == "") and (object_filter == "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date),
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter == "") and (object_filter == "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                status_task=status_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date),
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter != "") and (object_filter == "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                type_task=type_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date),
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter != "") and (object_filter != "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                status_task=status_filter,
                type_task=type_filter,
                object_task=object_filter
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter != "") and (object_filter == "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                status_task=status_filter,
                type_task=type_filter,
                business_trip=business_filter
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter != "") and (object_filter == "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                status_task=status_filter,
                type_task=type_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter != "") and (object_filter != "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                type_task=type_filter,
                object_task=object_filter,
                business_trip=business_filter
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter != "") and (object_filter == "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                type_task=type_filter,
                object_task=object_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter == "") and (object_filter != "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                object_task=object_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter != "") and (object_filter != "") and \
                (business_filter == "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                type_task=type_filter,
                object_task=object_filter
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter != "") and (object_filter != "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                type_task=type_filter,
                object_task=object_filter,
                business_trip=business_filter
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter != "") and (object_filter != "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                status_task=status_filter,
                type_task=type_filter,
                object_task=object_filter,
                business_trip=business_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter != "") and (object_filter != "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                type_task=type_filter,
                object_task=object_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter != "") and (object_filter == "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                type_task=type_filter,
                business_trip=business_filter
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter != "") and (object_filter == "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                type_task=type_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter == "") and (object_filter == "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter == "") and (object_filter != "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                object_task=object_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter != "") and (object_filter != "") and \
                (business_filter != "") and (start_date is None) and (end_date is None):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                type_task=type_filter,
                object_task=object_filter,
                business_trip=business_filter
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter != "") and (object_filter != "") and \
                (business_filter == "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                type_task=type_filter,
                object_task=object_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter != "") and (object_filter == "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                type_task=type_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter == "") and (object_filter != "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                object_task=object_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter != "") and (object_filter != "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                type_task=type_filter,
                object_task=object_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date)
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter != "") and (object_filter != "") and \
                (business_filter != "") and start_date and end_date:
            rows = Task.objects.filter(
                status_task=status_filter,
                type_task=type_filter,
                object_task=object_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date)
            )
        else:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                type_task=type_filter,
                object_task=object_filter,
                business_trip=business_filter,
                date_task__range=(start_date, end_date)
            )

        return rows.values_list(
            "id",
            "date_task",
            "time_task",
            "text_task",
            "object_task",
            "address_obj_task",
            "author_task",
            "employee_task",
            "urgency_task",
            "line_task",
            "status_task",
            "type_task",
            "business_trip",
            "note_task",
            "datetime_note_task"
        )

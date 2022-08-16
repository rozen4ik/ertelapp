import requests
from django.contrib.auth.models import User
from employee.models import Profile
from ertelapp import settings
from service import Service
from task.models import *
from counterparty.models import Counterparty


class TaskService(Service):
    tg_chat_id: str
    token_tg_bot: str

    def create_user_roles(self, dep_id):
        result = Profile.objects.get(position_dep_id_id=dep_id)
        return result

    def create_task(self, request):
        new_task = Task()
        new_task.date_task = request.POST.get("date_task")
        new_task.time_task = request.POST.get("time_task")
        new_task.text_task = request.POST.get("text_task")
        new_task.object_task = request.POST.get("object_task")
        new_task.author_task = request.user.first_name + " " + request.user.last_name
        new_task.employee_task = request.POST.get("employee_task")
        new_task.urgency_task = request.POST.get("urgency_task")
        new_task.line_task = request.POST.get("line_task")
        business_trip = request.POST.get("business_trip")
        if not business_trip:
            new_task.business_trip = "Не командировка"
        elif business_trip:
            new_task.business_trip = "Командировка"
        type_task = request.POST.get("type_task")
        if not type_task:
            new_task.type_task = "Офис"
            new_task.address_obj_task = "Москва, Бумажный пр., д. 14, корп. 1, офис 313"
            new_task.object_task = "Офис Эртел"
        elif type_task == "ГР":
            new_task.type_task = "Гарантийные работы"
            address_obj_task = Counterparty.objects.get(name=new_task.object_task)
            new_task.address_obj_task = address_obj_task.address
        elif type_task == "ТО":
            new_task.type_task = "Ежемесячное ТО"
            address_obj_task = Counterparty.objects.get(name=new_task.object_task)
            new_task.address_obj_task = address_obj_task.address
        elif type_task == "МР":
            new_task.type_task = "Монтажные работы"
            address_obj_task = Counterparty.objects.get(name=new_task.object_task)
            new_task.address_obj_task = address_obj_task.address
        elif type_task == "РПС":
            new_task.type_task = "Работы по счёту"
            address_obj_task = Counterparty.objects.get(name=new_task.object_task)
            new_task.address_obj_task = address_obj_task.address
        elif type_task == "ПНР":
            new_task.type_task = "Пусконаладочные работы"
            address_obj_task = Counterparty.objects.get(name=new_task.object_task)
            new_task.address_obj_task = address_obj_task.address
        new_task.save()
        self.send_message_telegram(new_task, "У вас новая задача!")

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

    def edit_task(self, request, task):
        task.date_task = request.POST.get("date_task")
        task.time_task = request.POST.get("time_task")
        task.text_task = request.POST.get("text_task")
        task.object_task = request.POST.get("object_task")
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
        type_task = request.POST.get("type_task")
        if not type_task:
            task.type_task = "Офис"
            task.address_obj_task = "Москва, Бумажный пр., д. 14, корп. 1, офис 313"
            task.object_task = "Офис Эртел"
        elif type_task == "ГР":
            task.type_task = "Гарантийные работы"
            address_obj_task = Counterparty.objects.get(name=task.object_task)
            task.address_obj_task = address_obj_task.address
        elif type_task == "ТО":
            task.type_task = "Ежемесячное ТО"
            address_obj_task = Counterparty.objects.get(name=task.object_task)
            task.address_obj_task = address_obj_task.address
        elif type_task == "МР":
            task.type_task = "Монтажные работы"
            address_obj_task = Counterparty.objects.get(name=task.object_task)
            task.address_obj_task = address_obj_task.address
        elif type_task == "РПС":
            task.type_task = "Работы по счёту"
            address_obj_task = Counterparty.objects.get(name=task.object_task)
            task.address_obj_task = address_obj_task.address
        elif type_task == "ПНР":
            task.type_task = "Пусконаладочные работы"
            address_obj_task = Counterparty.objects.get(name=task.object_task)
            task.address_obj_task = address_obj_task.address
        task.save()
        self.send_message_telegram(task, f"Задача №{task.id} изменилась!")

    def find_filter_task(self, filter_task):
        field_filter = (
            filter_task["employee_task"],
            filter_task["status_task"],
            filter_task["type_task"],
            filter_task["business_trip"]
        )
        employee_filter, status_filter, type_filter, business_filter = field_filter
        if (employee_filter == "") and (status_filter == "") and (type_filter == "") and (business_filter == ""):
            rows = Task.objects.all()
        elif (employee_filter != "") and (status_filter == "") and (type_filter == "") and (business_filter == ""):
            rows = Task.objects.filter(
                employee_task=employee_filter
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter == "") and (business_filter == ""):
            rows = Task.objects.filter(
                status_task=status_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter != "") and (business_filter == ""):
            rows = Task.objects.filter(
                type_task=type_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter == "") and (business_filter != ""):
            rows = Task.objects.filter(
                business_trip=business_filter
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter == "") and (business_filter == ""):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter != "") and (business_filter == ""):
            rows = Task.objects.filter(
                status_task=status_filter,
                type_task=type_filter
            )
        elif (employee_filter == "") and (status_filter == "") and (type_filter != "") and (business_filter != ""):
            rows = Task.objects.filter(
                type_task=type_filter,
                business_trip=business_filter
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter != "") and (business_filter == ""):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                type_task=type_filter,
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter == "") and (business_filter != ""):
            rows = Task.objects.filter(
                status_task=status_filter,
                business_trip=business_filter
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter == "") and (business_filter != ""):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                business_trip=business_filter
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter != "") and (business_filter == ""):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                type_task=type_filter,
            )
        elif (employee_filter != "") and (status_filter != "") and (type_filter == "") and (business_filter != ""):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                business_trip=business_filter
            )
        elif (employee_filter != "") and (status_filter == "") and (type_filter != "") and (business_filter != ""):
            rows = Task.objects.filter(
                employee_task=employee_filter,
                type_task=type_filter,
                business_trip=business_filter
            )
        elif (employee_filter == "") and (status_filter != "") and (type_filter != "") and (business_filter != ""):
            rows = Task.objects.filter(
                status_task=status_filter,
                type_task=type_filter,
                business_trip=business_filter
            )
        else:
            rows = Task.objects.filter(
                employee_task=employee_filter,
                status_task=status_filter,
                type_task=type_filter,
                business_trip=business_filter
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

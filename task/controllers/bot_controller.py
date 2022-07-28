import telebot
import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from ertelapp import settings
from task.models import *
from dadata import Dadata


class BotController:
    bot = telebot.TeleBot(settings.TOKEN_TG_BOT)
    location_employee = "Местоположение"

    # Формирование сообщения для отправки задачи исполнителю
    def get_message(self, task: Task) -> str:
        message_task = f"<b>Номер задачи:</b> {task.id}\n<b>Дата:</b> " \
                       f"{task.date_task}\n<b>Время:</b> {task.time_task}\n<b>Кто поручил:</b> " \
                       f"{task.author_task}\n<b>Статус задачи:</b> {task.status_task}\n<b>Задача:</b> " \
                       f"{task.text_task}\n<b>Место выполнения:</b> {task.address_task}\n" \
                       f"<b>Сроки выполнения:</b> {task.line_task}"
        return message_task

    # Поиск задачи по id
    def get_find_task(self, task_id: int) -> Task:
        task = Task.objects.get(id=task_id)
        return task

    # Поиск последней задачи
    def get_tasks(self, user):
        task = Task.objects.filter(Q(status_task="Выполняется") | Q(status_task="Отдано в разработку"),
                                   employee_task=f"{user.first_name} {user.last_name}")
        return task

    # Изменение статуса задачи
    def set_status_task(self, status_task: str, task: Task):
        task.status_task = status_task
        task.save()

    def set_location(self, location):
        self.location_employee = location

    # Получение местоположения
    def get_location(self) -> str:
        match self.location_employee:
            case "Местоположение":
                return "Местоположение не определено"
            case _:
                token_dadata = settings.TOKEN_DADATA
                dadata = Dadata(token_dadata)
                result = dadata.geolocate(name="address", lat=self.location_employee.location.latitude,
                                          lon=self.location_employee.location.longitude, count=1)
                result = result[0]
                result = result["value"]
                return result

    # Получение даты и времени
    def get_datetime(self) -> datetime:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M").split()
        return dt

    def create_work_task(self, task_id, msg_local):
        msg_date, msg_time = self.get_datetime()
        task = self.get_find_task(task_id)
        work_task = WorkTask()
        work_task.date_work_task = msg_date
        work_task.time_work_task = msg_time
        work_task.employee_work_task = f"{task.employee_task}"
        work_task.address_work_task = self.get_location()
        work_task.task_id = task.id
        work_task.status_work_task = msg_local
        work_task.save()

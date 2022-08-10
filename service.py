from django.core.paginator import Paginator
from task.models import Task


class Service:
    def paginator(self, model, number):
        page_model = Paginator(model, 10)
        return page_model.get_page(number)

    def get_objects_all(self, model):
        model = model.objects.all().order_by("-id")
        return model

    def get_object_deatil(self, model, id):
        model = model.objects.get(id=id)
        return model

    def get_message(self, task: Task) -> str:
        message_task = f"<b>Номер задачи:</b> {task.id}\n<b>Тип задачи:</b> {task.type_task}\n" \
                       f"<b>{task.business_trip}</b>\n<b>Дата:</b> " \
                       f"{task.date_task}\n<b>Время:</b> {task.time_task}\n<b>Кто поручил:</b> " \
                       f"{task.author_task}\n<b>Статус задачи:</b> {task.status_task}\n<b>Задача:</b> " \
                       f"{task.text_task}\n<b>Объект:</b> {task.object_task}\n" \
                       f"<b>Адрес:</b> {task.address_obj_task}\n<b>Приоритет:</b> {task.urgency_task}\n"\
                       f"<b>Сроки выполнения:</b> {task.line_task}"
        return message_task
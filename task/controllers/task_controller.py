from task.models import *


class TaskController:
    tg_chat_id: str
    token_tg_bot: str

    def get_objects_all(self, model):
        model = model.objects.all().order_by("-id")
        return model

    def get_detail_object(self, model, id):
        model = model.objects.get(id=id)
        return model

    def create_task(self, request):
        new_task = Task()
        new_task.date_task = request.POST.get("date_task")
        new_task.time_task = request.POST.get("time_task")
        new_task.text_task = request.POST.get("text_task")
        new_task.address_task = request.POST.get("address_task")
        new_task.author_task = request.user.first_name + " " + request.user.last_name
        new_task.employee_task = request.POST.get("employee_task")
        new_task.line_task = request.POST.get("line_task")
        business_trip = request.POST.get("business_trip")
        if not business_trip:
            new_task.business_trip = "Не командировка"
        elif business_trip:
            new_task.business_trip = "Командировка"
        type_task = request.POST.get("type_task")
        if not type_task:
            new_task.type_task = "Офис"
        elif type_task == "ГР":
            new_task.type_task = "Гарантийные работы"
        elif type_task == "ТО":
            new_task.type_task = "Ежемесячное ТО"
        # elif type_task == "Офис":
        #     new_task.type_task = "Офис"
        new_task.save()

    def edit_task(self, request, task):
        task.date_task = request.POST.get("date_task")
        task.time_task = request.POST.get("time_task")
        task.text_task = request.POST.get("text_task")
        task.address_task = request.POST.get("address_task")
        task.author_task = request.user.first_name + " " + request.user.last_name
        task.employee_task = request.POST.get("employee_task")
        task.line_task = request.POST.get("line_task")
        task.status_task = request.POST.get("status_task")
        task.save()

    def create_counterparty(self, request, model):
        new_counterparty = model()
        new_counterparty.name = request.POST.get("name")
        new_counterparty.type = request.POST.get("type")
        new_counterparty.contract = request.POST.get("contract")
        new_counterparty.address = request.POST.get("address")
        new_counterparty.save()

    def get_tg_chat_id(self):
        return self.tg_chat_id

    def set_tg_chat_id(self, chat_id):
        self.tg_chat_id = chat_id

    def get_token_tg_bot(self):
        return self.token_tg_bot

    def set_token_tg_bot(self, tg_bot):
        self.token_tg_bot = tg_bot

    def update_dict_task(self, dict_task):
        dict_task["tg_chat_id"] = self.get_tg_chat_id()
        dict_task["token_tg_bot"] = self.get_token_tg_bot()


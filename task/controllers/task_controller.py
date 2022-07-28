from task.models import *


class TaskController:
    tg_chat_id: str
    token_tg_bot: str

    task = Task.objects.all().order_by("-id")
    users = User.objects.all().select_related('profile')
    director_user = Profile.objects.get(position_dep_id_id=1)
    eng_user = Profile.objects.get(position_dep_id_id=7)
    sales_user = Profile.objects.get(position_dep_id_id=2)
    technical_user = Profile.objects.get(position_dep_id_id=3)
    accounting_user = Profile.objects.get(position_dep_id_id=11)
    personnel_user = Profile.objects.get(position_dep_id_id=13)
    engineering_task = Task.objects.filter(author_task=eng_user).order_by("-id")
    sales_task = Task.objects.filter(author_task=sales_user).order_by("-id")
    technical_task = Task.objects.filter(author_task=technical_user).order_by("-id")
    accounting_task = Task.objects.filter(author_task=accounting_user).order_by("-id")
    personnel_task = Task.objects.filter(author_task=personnel_user).order_by("-id")



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
            new_task.business_trip = False
        elif business_trip:
            new_task.business_trip = True
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


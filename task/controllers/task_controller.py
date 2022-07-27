from task.models import *


class TaskController:
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

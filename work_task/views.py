from django.http import HttpResponseNotFound
from django.shortcuts import render
from service import Service
from work_task.models import WorkTask

work_task_service = Service()


# Create your views here.
def index_bot(request):
    work_task = work_task_service.get_objects_all(WorkTask)
    return render(request, "work_task/work_task.html", {"work_task": work_task})


def show_work_task_for_task(request, id):
    try:
        work_task_employee = WorkTask.objects.filter(task=id).order_by("-id")
        return render(request, "work_task/work_task_employee.html", {"work_task_employee": work_task_employee})
    except WorkTask.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from task.controllers.task_controller import TaskController
from work_task.models import WorkTask

task_controller = TaskController()


# Create your views here.
def index_bot(request):
    work_task = task_controller.get_objects_all(WorkTask)
    return render(request, "work_task/work_task.html", {"work_task": work_task})


# Удаление записи в в разделе контроля выполнения работ
def delete_work_task(request, id):
    try:
        work_task = task_controller.get_detail_object(WorkTask, id)
        work_task.delete()
        return HttpResponseRedirect("/work_task/")
    except WorkTask.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


def show_work_task_for_task(request, id):
    try:
        work_task_employee = WorkTask.objects.filter(task=id).order_by("-id")
        return render(request, "work_task/work_task_employee.html", {"work_task_employee": work_task_employee})
    except WorkTask.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")

from django.http import HttpResponseNotFound
from django.shortcuts import render
from history.models import HistoryNoteTask, HistoryStatusTask
from service import Service

history_service = Service()


def history_note_task_detail(request, id):
    try:
        history = HistoryNoteTask.objects.filter(task=id).order_by("-id")
        data = {
            "history": history
        }
        return render(request, "history/history_note_task/history_note_task_employee.html", data)
    except HistoryNoteTask.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")


def history_status_task_detail(request, id):
    try:
        history = HistoryStatusTask.objects.filter(task=id).order_by("-id")
        data = {
            "history": history
        }
        return render(request, "history/history_status_task/history_status_task_employee.html", data)
    except HistoryStatusTask.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")

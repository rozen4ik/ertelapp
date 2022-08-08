import datetime
import xlwt
from django.http import HttpResponseNotFound, HttpResponse
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


# Реализация экспорта данных в excel таблицы WorkTask
def export_excel_work_task(request):
    response = HttpResponse(content_type="applications/ms-excel")
    response["Content-Disposition"] = "attachment; filename=work_task" + str(datetime.datetime.now()) + ".xls"

    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("report")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        "#",
        "Дата",
        "Время",
        "Исполнитель",
        "Местонахождение",
        "Статус исполнителя",
        "Номер задачи"
    ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    rows = WorkTask.objects.all().values_list(
        "id",
        "date_work_task",
        "time_work_task",
        "employee_work_task",
        "address_work_task",
        "status_work_task",
        "task"
    )

    rows = rows.order_by("-id")

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

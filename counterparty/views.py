from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from counterparty.models import CounterpartyTO, CounterpartyWarrantyObligations
from task.services.task_service import TaskService


task_service = TaskService()


# Create your views here.
def counterparty_to(request):
    page_number = request.GET.get("page")
    counterparty = task_service.get_objects_all(CounterpartyTO)
    page_m = task_service.paginator(counterparty, page_number)
    data = {
        "counterparty": counterparty,
        "page_m": page_m
    }
    return render(request, "counterparty/counterparty_to/counterparty_to.html", data)


def counterparty_warranty_obligations(request):
    page_number = request.GET.get("page")
    counterparty = task_service.get_objects_all(CounterpartyWarrantyObligations)
    page_m = task_service.paginator(counterparty, page_number)
    data = {
        "counterparty": counterparty,
        "page_m": page_m
    }
    return render(request, "counterparty/counterparty_warranty_obligations/counterparty_warranty_obligations.html", data)


def create_counterparty_to(request):
    if request.method == "POST":
        task_service.create_counterparty(request, CounterpartyTO)
    return HttpResponseRedirect("/counterparty_to/")


def create_countrparty_warranty_obligations(request):
    if request.method == "POST":
        task_service.create_counterparty(request, CounterpartyWarrantyObligations)
    return HttpResponseRedirect("/counterparty_warranty_obligations/")


def counterparty_to_detail(request, id):
    try:
        counterparty = task_service.get_detail_object(CounterpartyTO, id)
        return render(request, "counterparty/counterparty.html", {"counterparty": counterparty})
    except CounterpartyTO.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")


def countrparty_warranty_obligations_detail(request, id):
    try:
        counterparty = task_service.get_detail_object(CounterpartyWarrantyObligations, id)
        return render(request, "counterparty/counterparty.html", {"counterparty": counterparty})
    except CounterpartyWarrantyObligations.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from counterparty.models import CounterpartyTO, CountrpartyWarrantyObligations
from task.controllers.task_controller import TaskController
from task.views import paginator


task_controller = TaskController()


# Create your views here.
def counterparty_to(request):
    page_number = request.GET.get("page")
    counterparty = task_controller.get_objects_all(CounterpartyTO)
    page_m = paginator(counterparty, page_number)
    data = {
        "counterparty": counterparty,
        "page_m": page_m
    }
    return render(request, "countrparty/countrparty_to/countrparty_to.html", data)


def countrparty_warranty_obligations(request):
    page_number = request.GET.get("page")
    counterparty = task_controller.get_objects_all(CountrpartyWarrantyObligations)
    page_m = paginator(counterparty, page_number)
    data = {
        "counterparty": counterparty,
        "page_m": page_m
    }
    return render(request, "countrparty/countrparty_warranty_obligations/countrparty_warranty_obligations.html", data)


def create_counterparty_to(request):
    if request.method == "POST":
        task_controller.create_counterparty(request, CounterpartyTO)
    return HttpResponseRedirect("/counterparty_to/")


def create_countrparty_warranty_obligations(request):
    if request.method == "POST":
        task_controller.create_counterparty(request, CountrpartyWarrantyObligations)
    return HttpResponseRedirect("/countrparty_warranty_obligations/")


def counterparty_to_detail(request, id):
    try:
        counterparty = task_controller.get_detail_object(CounterpartyTO, id)
        return render(request, "countrparty/counterparty.html", {"counterparty": counterparty})
    except CounterpartyTO.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")


def countrparty_warranty_obligations_detail(request, id):
    try:
        counterparty = task_controller.get_detail_object(CountrpartyWarrantyObligations, id)
        return render(request, "countrparty/counterparty.html", {"counterparty": counterparty})
    except CountrpartyWarrantyObligations.DoesNotExist:
        return HttpResponseNotFound("<h2>WorkTask not found</h2>")

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from counterparty.models import CounterpartyTO, CounterpartyWarrantyObligations, Counterparty
from counterparty.services.counterparty_service import CounterpartyService

counterparty_service = CounterpartyService()


def list_counterparty(request):
    page_number = request.GET.get("page")
    counterparty = counterparty_service.get_objects_all(Counterparty)
    page_m = counterparty_service.paginator(counterparty, page_number)
    data = {
        "counterparty": counterparty,
        "page_m": page_m
    }

    return render(request, "counterparty/counterparty.html", data)


def create_counterparty(request):
    if request.method == "POST":
        counterparty_service.create_counterparty(request, Counterparty)
    return HttpResponseRedirect("/counterparty/")


def edit_counterparty(request, id):
    try:
        counterparty = counterparty_service.get_object_deatil(Counterparty, id)
        users = counterparty_service.get_objects_all(User).select_related('profile')

        data = {
            "counterparty": counterparty,
            "users": users,
        }

        if request.method == "POST":
            counterparty_service.edit_counterparty(request, counterparty)
            return HttpResponseRedirect("/")
        else:
            return render(request, "counterparty/edit.html", data)

    except CounterpartyTO.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


def counterparty_to(request):
    page_number = request.GET.get("page")
    counterparty = counterparty_service.get_objects_all(CounterpartyTO)
    page_m = counterparty_service.paginator(counterparty, page_number)
    data = {
        "counterparty": counterparty,
        "page_m": page_m
    }
    return render(request, "counterparty/counterparty_to/counterparty_to.html", data)


def counterparty_warranty_obligations(request):
    page_number = request.GET.get("page")
    counterparty = counterparty_service.get_objects_all(CounterpartyWarrantyObligations)
    page_m = counterparty_service.paginator(counterparty, page_number)
    data = {
        "counterparty": counterparty,
        "page_m": page_m
    }
    return render(request, "counterparty/counterparty_warranty_obligations/counterparty_warranty_obligations.html",
                  data)


def create_counterparty_to(request):
    if request.method == "POST":
        counterparty_service.create_counterparty(request, CounterpartyTO)
    return HttpResponseRedirect("/counterparty_to/")


def create_counterparty_warranty_obligations(request):
    if request.method == "POST":
        counterparty_service.create_counterparty(request, CounterpartyWarrantyObligations)
    return HttpResponseRedirect("/counterparty_warranty_obligations/")


# Изменение данных
def edit_counterparty_to(request, id):
    try:
        edit_counterparty_to = counterparty_service.get_object_deatil(CounterpartyTO, id)
        users = counterparty_service.get_objects_all(User).select_related('profile')

        data = {
            "edit_counterparty_to": edit_counterparty_to,
            "users": users,
        }

        if request.method == "POST":
            counterparty_service.edit_counterparty(request, edit_counterparty_to)
            return HttpResponseRedirect("/")
        else:
            return render(request, "counterparty/counterparty_to/edit.html", data)

    except CounterpartyTO.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")


def edit_counterparty_warranty_obligations(request, id):
    try:
        edit_counterparty_warranty_obligations = counterparty_service.get_object_deatil(
            CounterpartyWarrantyObligations, id)
        users = counterparty_service.get_objects_all(User).select_related('profile')

        data = {
            "edit_counterparty_warranty_obligations": edit_counterparty_warranty_obligations,
            "users": users,
        }

        if request.method == "POST":
            counterparty_service.edit_counterparty(request, edit_counterparty_warranty_obligations)
            return HttpResponseRedirect("/")
        else:
            return render(request, "counterparty/counterparty_warranty_obligations/edit.html", data)

    except CounterpartyWarrantyObligations.DoesNotExist:
        return HttpResponseNotFound("<h2>Task not found</h2>")

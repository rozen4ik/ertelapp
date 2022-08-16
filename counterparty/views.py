from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from counterparty.models import Counterparty
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

    except Counterparty.DoesNotExist:
        return HttpResponseNotFound("<h2>Counterparty not found</h2>")

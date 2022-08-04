from service import Service


class CounterpartyService(Service):
    def create_counterparty(self, request, model):
        new_counterparty = model()
        new_counterparty.name = request.POST.get("name")
        new_counterparty.type = request.POST.get("type")
        new_counterparty.contract = request.POST.get("contract")
        new_counterparty.address = request.POST.get("address")
        new_counterparty.save()

    def edit_counterparty(self, request, counterparty):
        counterparty.name = request.POST.get("name")
        counterparty.type = request.POST.get("type")
        counterparty.contract = request.POST.get("contract")
        counterparty.address = request.POST.get("address")
        counterparty.save()

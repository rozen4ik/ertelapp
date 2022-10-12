from service import Service


class CounterpartyService(Service):
    def counterparty_layout(self, request, counterparty):
        counterparty.name = request.POST.get("name")
        counterparty.work_name = request.POST.get("work_name")
        counterparty.type = request.POST.get("type")
        counterparty.contract = request.POST.get("contract")
        counterparty.address = request.POST.get("address")
        counterparty.save()

    def create_counterparty(self, request, model):
        new_counterparty = model()
        self.counterparty_layout(request, new_counterparty)

    def edit_counterparty(self, request, counterparty):
        self.counterparty_layout(request, counterparty)

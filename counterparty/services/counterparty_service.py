from django.core.paginator import Paginator


class CounterpartyService:
    def paginator(self, model, number):
        page_model = Paginator(model, 10)
        return page_model.get_page(number)

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

    def get_objects_all(self, model):
        model = model.objects.all().order_by("-id")
        return model

    def get_detail_object(self, model, id):
        model = model.objects.get(id=id)
        return model
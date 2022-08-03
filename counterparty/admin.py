from django.contrib import admin

from counterparty.models import CounterpartyTO, CounterpartyWarrantyObligations


class CounterpartyTOAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "contract", "address")
    list_filter = ["type"]


class CountrpartyWarrantyObligationsAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "contract", "address")
    list_filter = ["type"]


admin.site.register(CounterpartyTO, CounterpartyTOAdmin)
admin.site.register(CounterpartyWarrantyObligations, CountrpartyWarrantyObligationsAdmin)
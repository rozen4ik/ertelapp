from django.contrib import admin

from counterparty.models import CounterpartyTO, CounterpartyWarrantyObligations


@admin.register(CounterpartyTO)
class CounterpartyTOAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "contract", "address")
    list_display_links = ("id", "name", "type", "contract", "address")
    list_filter = ["type"]


@admin.register(CounterpartyWarrantyObligations)
class CounterpartyWarrantyObligationsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "contract", "address")
    list_display_links = ("id", "name", "type", "contract", "address")
    list_filter = ["type"]


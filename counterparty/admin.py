from django.contrib import admin
from counterparty.models import Counterparty


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "contract", "address")
    list_display_links = ("id", "name", "type", "contract", "address")
    list_filter = ["type"]

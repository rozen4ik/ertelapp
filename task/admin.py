from django.contrib import admin
from .models import *


class CounterpartyTOAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "contract", "address")
    list_filter = ["type"]


class CountrpartyWarrantyObligationsAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "contract", "address")
    list_filter = ["type"]


# Register your models here.
admin.site.register(Task)
admin.site.register(Profile)
admin.site.register(WorkTask)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(CounterpartyTO, CounterpartyTOAdmin)
admin.site.register(CountrpartyWarrantyObligations, CountrpartyWarrantyObligationsAdmin)

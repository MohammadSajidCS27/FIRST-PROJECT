from django.contrib import admin
from .models import FundingSource, CashBookEntry


@admin.register(FundingSource)
class FundingSourceAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(CashBookEntry)
class CashBookEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "entry_type", "amount", "source", "description")
    list_filter = ("entry_type", "source")
    search_fields = ("description",)

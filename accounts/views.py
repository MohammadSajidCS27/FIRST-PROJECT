from django.shortcuts import render
from django import forms
from .models import CashBookEntry, FundingSource


class CashBookEntryForm(forms.ModelForm):
    class Meta:
        model = CashBookEntry
        fields = ["date", "description", "entry_type", "amount", "source"]


def cashbook_summary(request):
    totals = CashBookEntry.totals()
    entries = CashBookEntry.objects.select_related("source").all()[:100]
    return render(request, "accounts/cashbook_summary.html", {"totals": totals, "entries": entries})


def cashbook_add(request):
    if request.method == "POST":
        form = CashBookEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "accounts/cashbook_add.html", {"form": CashBookEntryForm(), "saved": True})
    else:
        form = CashBookEntryForm()
    return render(request, "accounts/cashbook_add.html", {"form": form})

# Create your views here.

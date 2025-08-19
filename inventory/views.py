from django.shortcuts import render
from django import forms
from .models import InventoryItem, Location


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["identifier", "name", "category", "location", "quantity", "notes"]


def inventory_list(request):
    items = InventoryItem.objects.select_related("location").all()
    return render(request, "inventory/inventory_list.html", {"items": items})


def inventory_add(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "inventory/inventory_add.html", {"form": InventoryItemForm(), "saved": True})
    else:
        form = InventoryItemForm()
    return render(request, "inventory/inventory_add.html", {"form": form})

# Create your views here.

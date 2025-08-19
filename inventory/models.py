from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class InventoryItem(models.Model):
    CATEGORY_CHOICES = (
        ("EQUIPMENT", "Equipment"),
        ("FURNITURE", "Furniture"),
        ("BOOK", "Book"),
        ("OTHER", "Other"),
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    identifier = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.identifier} - {self.name}"

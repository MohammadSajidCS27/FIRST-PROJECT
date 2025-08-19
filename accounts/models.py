from django.db import models
from django.utils import timezone


class FundingSource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class CashBookEntry(models.Model):
    ENTRY_TYPES = (
        ("INCOME", "Income"),
        ("EXPENDITURE", "Expenditure"),
    )
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255)
    entry_type = models.CharField(max_length=12, choices=ENTRY_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.ForeignKey(FundingSource, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.date} {self.entry_type} {self.amount}"

    class Meta:
        ordering = ["-date", "-id"]

    @staticmethod
    def totals():
        income = sum(e.amount for e in CashBookEntry.objects.filter(entry_type="INCOME"))
        expenditure = sum(e.amount for e in CashBookEntry.objects.filter(entry_type="EXPENDITURE"))
        balance = (income or 0) - (expenditure or 0)
        return {"income": float(income or 0), "expenditure": float(expenditure or 0), "balance": float(balance)}

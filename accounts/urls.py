from django.urls import path
from . import views


urlpatterns = [
    path("cashbook/", views.cashbook_summary, name="cashbook_summary"),
    path("cashbook/add/", views.cashbook_add, name="cashbook_add"),
]


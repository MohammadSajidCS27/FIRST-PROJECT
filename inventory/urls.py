from django.urls import path
from . import views


urlpatterns = [
    path("", views.inventory_list, name="inventory_list"),
    path("add/", views.inventory_add, name="inventory_add"),
]


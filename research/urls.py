from django.urls import path
from . import views


urlpatterns = [
    path("projects/", views.project_list, name="project_list"),
    path("projects/add/", views.project_add, name="project_add"),
    path("publications/", views.publication_list, name="publication_list"),
    path("publications/add/", views.publication_add, name="publication_add"),
]


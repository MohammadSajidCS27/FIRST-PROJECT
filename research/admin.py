from django.contrib import admin
from .models import Faculty, ResearchProject, Publication


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")


@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "principal_investigator", "start_date", "end_date")
    list_filter = ("start_date", "end_date")
    search_fields = ("title",)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "venue", "year", "project")
    list_filter = ("year",)
    search_fields = ("title", "venue")

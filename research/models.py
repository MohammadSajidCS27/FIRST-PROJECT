from django.db import models
from django.utils import timezone


class Faculty(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.name


class ResearchProject(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    principal_investigator = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name="lead_projects")
    members = models.ManyToManyField(Faculty, related_name="projects", blank=True)
    summary = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title


class Publication(models.Model):
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    project = models.ForeignKey(ResearchProject, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title} ({self.year})"

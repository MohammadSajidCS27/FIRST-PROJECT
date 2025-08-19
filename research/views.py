from django.shortcuts import render
from django import forms
from .models import ResearchProject, Publication, Faculty


class ProjectForm(forms.ModelForm):
    class Meta:
        model = ResearchProject
        fields = ["title", "start_date", "end_date", "principal_investigator", "members", "summary"]


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ["title", "authors", "venue", "year", "project"]


def project_list(request):
    projects = ResearchProject.objects.select_related("principal_investigator").prefetch_related("members").all()
    return render(request, "research/project_list.html", {"projects": projects})


def project_add(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "research/project_add.html", {"form": ProjectForm(), "saved": True})
    else:
        form = ProjectForm()
    return render(request, "research/project_add.html", {"form": form})


def publication_list(request):
    pubs = Publication.objects.select_related("project").all()
    return render(request, "research/publication_list.html", {"publications": pubs})


def publication_add(request):
    if request.method == "POST":
        form = PublicationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "research/publication_add.html", {"form": PublicationForm(), "saved": True})
    else:
        form = PublicationForm()
    return render(request, "research/publication_add.html", {"form": form})

# Create your views here.

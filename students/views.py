from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from .models import Student, Course, Semester, Enrollment
from django import forms


class StudentLookupForm(forms.Form):
    roll_number = forms.CharField(label="Roll Number", max_length=20)


class RegistrationForm(forms.Form):
    roll_number = forms.CharField(label="Roll Number", max_length=20)
    semester = forms.ModelChoiceField(queryset=Semester.objects.all())
    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.CheckboxSelectMultiple)


class GradeEntryForm(forms.Form):
    enrollment_id = forms.IntegerField(widget=forms.HiddenInput)
    grade_letter = forms.ChoiceField(choices=Enrollment.GRADE_CHOICES)


def student_lookup(request):
    context = {}
    form = StudentLookupForm(request.GET or None)
    student = None
    enrollments = []
    if form.is_valid():
        roll_number = form.cleaned_data["roll_number"].strip()
        student = get_object_or_404(Student, roll_number=roll_number)
        enrollments = (
            Enrollment.objects.filter(student=student)
            .select_related("course", "semester")
            .order_by("semester__year", "semester__term", "course__code")
        )
    context.update({"form": form, "student": student, "enrollments": enrollments})
    return render(request, "students/student_lookup.html", context)


def course_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            student = get_object_or_404(Student, roll_number=form.cleaned_data["roll_number"].strip())
            semester = form.cleaned_data["semester"]
            for course in form.cleaned_data["courses"]:
                Enrollment.objects.get_or_create(student=student, course=course, semester=semester)
            return redirect("student_lookup")
    else:
        form = RegistrationForm()
    return render(request, "students/course_registration.html", {"form": form})


def grade_entry(request):
    pending = Enrollment.objects.filter(grade_letter__isnull=True).select_related("student", "course", "semester")
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("grade_") and value:
                enrollment_id = int(key.split("_")[1])
                try:
                    enrollment = Enrollment.objects.get(id=enrollment_id)
                except Enrollment.DoesNotExist:
                    continue
                enrollment.grade_letter = value
                enrollment.save()
        return redirect("grade_entry")
    return render(request, "students/grade_entry.html", {"pending": pending, "grade_choices": [c[0] for c in Enrollment.GRADE_CHOICES]})


def grade_sheet(request):
    form = StudentLookupForm(request.GET or None)
    student = None
    semester = None
    enrollments = []
    gpa = None
    cgpa = None
    if form.is_valid() and request.GET.get("semester"):
        roll_number = form.cleaned_data["roll_number"].strip()
        student = get_object_or_404(Student, roll_number=roll_number)
        semester_id = request.GET.get("semester")
        semester = get_object_or_404(Semester, id=semester_id)
        enrollments = Enrollment.objects.filter(student=student, semester=semester).select_related("course")
        gpa = student.calculate_semester_gpa(semester)
        cgpa = student.calculate_cgpa()
    semesters = Semester.objects.all().order_by("year", "term")
    return render(request, "students/grade_sheet.html", {"form": form, "student": student, "semester": semester, "semesters": semesters, "enrollments": enrollments, "gpa": gpa, "cgpa": cgpa})

# Create your views here.

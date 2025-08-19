from django.contrib import admin
from .models import Student, Course, Semester, Enrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("roll_number", "full_name", "date_of_admission")
    search_fields = ("roll_number", "full_name")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "credits")
    search_fields = ("code", "title")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("name", "term", "year")
    list_filter = ("term", "year")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "semester", "grade_letter", "grade_point")
    list_filter = ("semester", "grade_letter")
    search_fields = ("student__roll_number", "course__code")

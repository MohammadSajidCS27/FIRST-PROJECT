from django.urls import path
from . import views


urlpatterns = [
    path("lookup/", views.student_lookup, name="student_lookup"),
    path("register/", views.course_registration, name="course_registration"),
    path("grade-entry/", views.grade_entry, name="grade_entry"),
    path("grade-sheet/", views.grade_sheet, name="grade_sheet"),
]


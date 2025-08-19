from django.db import models
from django.utils import timezone


class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    date_of_admission = models.DateField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.roll_number} - {self.full_name}"

    def calculate_semester_gpa(self, semester: "Semester") -> float:
        enrollments = Enrollment.objects.filter(student=self, semester=semester, grade_point__isnull=False)
        total_credits = sum(e.course.credits for e in enrollments)
        if total_credits == 0:
            return 0.0
        weighted_points = sum((e.grade_point or 0) * e.course.credits for e in enrollments)
        return round(float(weighted_points) / float(total_credits), 2)

    def calculate_cgpa(self) -> float:
        enrollments = Enrollment.objects.filter(student=self, grade_point__isnull=False)
        total_credits = sum(e.course.credits for e in enrollments)
        if total_credits == 0:
            return 0.0
        weighted_points = sum((e.grade_point or 0) * e.course.credits for e in enrollments)
        return round(float(weighted_points) / float(total_credits), 2)

    def get_backlogs(self):
        return Enrollment.objects.filter(student=self).filter(models.Q(grade_letter__isnull=True) | models.Q(grade_point__lt=5))


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    credits = models.PositiveIntegerField(default=3)

    def __str__(self) -> str:
        return f"{self.code} - {self.title} ({self.credits})"


class Semester(models.Model):
    TERM_CHOICES = [
        ("SPRING", "Spring"),
        ("SUMMER", "Summer"),
        ("FALL", "Fall"),
    ]
    name = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    start_date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ("year", "term")

    def __str__(self) -> str:
        return f"{self.name} ({self.term} {self.year})"


def grade_letter_to_points(letter: str) -> int:
    mapping = {
        "O": 10,
        "A+": 9,
        "A": 8,
        "B+": 7,
        "B": 6,
        "C": 5,
        "F": 0,
    }
    return mapping.get(letter, 0)


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    registered_on = models.DateField(default=timezone.now)

    GRADE_CHOICES = [
        ("O", "O"),
        ("A+", "A+"),
        ("A", "A"),
        ("B+", "B+"),
        ("B", "B"),
        ("C", "C"),
        ("F", "F"),
    ]
    grade_letter = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    grade_point = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    class Meta:
        unique_together = ("student", "course", "semester")

    def __str__(self) -> str:
        return f"{self.student.roll_number} - {self.course.code} ({self.semester})"

    def save(self, *args, **kwargs):
        if self.grade_letter and self.grade_point is None:
            self.grade_point = grade_letter_to_points(self.grade_letter)
        super().save(*args, **kwargs)

    @property
    def is_passed(self) -> bool:
        return (self.grade_point or 0) >= 5

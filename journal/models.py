from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Müəllim'),
        ('student', 'Tələbə'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'

    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Fənn adı")

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="Qrup adı")

    def __str__(self):
        return self.name

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subjects = models.ManyToManyField(Subject, verbose_name="Tədris etdiyi fənlər")
    groups = models.ManyToManyField(Group, verbose_name="Tədris etdiyi qruplar")

    def __str__(self):
        return f"{self.user.get_full_name()} (Müəllim)"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, verbose_name="Qrup")

    def __str__(self):
        return f"{self.user.get_full_name()} (Tələbə)"

class Grade(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    
    midterm = models.IntegerField(default=0, verbose_name="Midterm (20)")
    presentation = models.IntegerField(default=0, verbose_name="Təqdimat (20)")
    activity = models.IntegerField(default=0, verbose_name="Aktivlik (10)")
    final = models.IntegerField(default=0, verbose_name="Final (50)")

    class Meta:
        unique_together = ('student', 'subject')

    def calculate_pre_exam(self):
        return self.midterm + self.presentation + self.activity

    def calculate_total(self):
        return self.calculate_pre_exam() + self.final

    def is_passed(self):
        return self.calculate_total() >= 51

    def get_letter_grade(self):
        total = self.calculate_total()
        if total >= 91:
            return 'A'
        elif total >= 81:
            return 'B'
        elif total >= 71:
            return 'C'
        elif total >= 61:
            return 'D'
        elif total >= 51:
            return 'E'
        else:
            return 'F'

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject.name}"

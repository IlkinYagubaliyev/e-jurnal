from django.core.management.base import BaseCommand
from journal.models import User, Subject, Group, TeacherProfile, StudentProfile, Grade
import random

class Command(BaseCommand):
    help = 'Setup test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')

        # Create Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
            self.stdout.write('Admin created (admin/admin123)')

        # Create Subjects
        math, _ = Subject.objects.get_or_create(name='Riyaziyyat')
        physics, _ = Subject.objects.get_or_create(name='Fizika')
        
        # Create Group
        group_a1, _ = Group.objects.get_or_create(name='A1')

        # Create Teacher
        if not User.objects.filter(username='teacher').exists():
            teacher_user = User.objects.create_user('teacher', 'teacher@example.com', 'teacher123', role='teacher', first_name='Ali', last_name='Aliyev')
            teacher_profile = TeacherProfile.objects.create(user=teacher_user)
            teacher_profile.subjects.add(math, physics)
            teacher_profile.groups.add(group_a1)
            self.stdout.write('Teacher created (teacher/teacher123)')

        # Create Students
        for i in range(1, 3):
            username = f'student{i}'
            if not User.objects.filter(username=username).exists():
                student_user = User.objects.create_user(username, f'{username}@example.com', 'student123', role='student', first_name=f'Tələbə', last_name=f'{i}')
                StudentProfile.objects.create(user=student_user, group=group_a1)
                self.stdout.write(f'Student created ({username}/student123)')

        # Create Grades (Random)
        students = StudentProfile.objects.all()
        subjects = [math, physics]
        
        for student in students:
            for subject in subjects:
                grade, created = Grade.objects.get_or_create(student=student, subject=subject)
                if created:
                    grade.midterm = random.randint(10, 20)
                    grade.presentation = random.randint(10, 20)
                    grade.activity = random.randint(5, 10)
                    grade.final = random.randint(30, 50)
                    grade.save()
        
        self.stdout.write(self.style.SUCCESS('Test data created successfully!'))

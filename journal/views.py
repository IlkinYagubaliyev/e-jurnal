from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import User, TeacherProfile, StudentProfile, Subject, Group, Grade
from .forms import StudentCreationForm, TeacherCreationForm, SubjectForm, GroupForm, TeacherAssignmentForm

class CustomLoginView(LoginView):
    template_name = 'journal/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_admin():
            return reverse_lazy('admin_dashboard')
        elif user.is_teacher():
            return reverse_lazy('teacher_dashboard')
        elif user.is_student():
            return reverse_lazy('student_dashboard')
        return reverse_lazy('home')

@login_required
def home(request):
    if request.user.is_admin():
        return redirect('admin_dashboard')
    elif request.user.is_teacher():
        return redirect('teacher_dashboard')
    elif request.user.is_student():
        return redirect('student_dashboard')
    return render(request, 'journal/home.html') # Fallback

@login_required
def admin_dashboard(request):
    if not request.user.is_admin():
        return redirect('home')
    
    context = {
        'student_count': StudentProfile.objects.count(),
        'teacher_count': TeacherProfile.objects.count(),
        'subject_count': Subject.objects.count(),
        'group_count': Group.objects.count(),
    }
    return render(request, 'journal/admin_dashboard.html', context)

@login_required
def create_student(request):
    if not request.user.is_admin():
        return redirect('home')
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = StudentCreationForm()
    return render(request, 'journal/form.html', {'form': form, 'title': 'Yeni Tələbə'})

@login_required
def create_teacher(request):
    if not request.user.is_admin():
        return redirect('home')
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = TeacherCreationForm()
    return render(request, 'journal/form.html', {'form': form, 'title': 'Yeni Müəllim'})

@login_required
def create_subject(request):
    if not request.user.is_admin():
        return redirect('home')
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = SubjectForm()
    return render(request, 'journal/form.html', {'form': form, 'title': 'Yeni Fənn'})

@login_required
def create_group(request):
    if not request.user.is_admin():
        return redirect('home')
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = GroupForm()
    return render(request, 'journal/form.html', {'form': form, 'title': 'Yeni Qrup'})

@login_required
def assign_teacher(request, teacher_id):
    if not request.user.is_admin():
        return redirect('home')
    teacher = get_object_or_404(TeacherProfile, id=teacher_id)
    if request.method == 'POST':
        form = TeacherAssignmentForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = TeacherAssignmentForm(instance=teacher)
    return render(request, 'journal/form.html', {'form': form, 'title': f'Təyinat: {teacher.user.get_full_name()}'})

@login_required
def teacher_list(request):
    if not request.user.is_admin():
        return redirect('home')
    teachers = TeacherProfile.objects.all()
    return render(request, 'journal/teacher_list.html', {'teachers': teachers})

@login_required
def student_list(request):
    if not request.user.is_admin():
        return redirect('home')
    students = StudentProfile.objects.all()
    return render(request, 'journal/student_list.html', {'students': students})

@login_required
def subject_list(request):
    if not request.user.is_admin():
        return redirect('home')
    subjects = Subject.objects.all()
    return render(request, 'journal/subject_list.html', {'subjects': subjects})

@login_required
def group_list(request):
    if not request.user.is_admin():
        return redirect('home')
    groups = Group.objects.all()
    return render(request, 'journal/group_list.html', {'groups': groups})

@login_required
def edit_student(request, student_id):
    if not request.user.is_admin():
        return redirect('home')
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == 'POST':
        form = StudentCreationForm(request.POST, instance=student.user)
        if form.is_valid():
            user = form.save()
            student.group = form.cleaned_data.get('group')
            student.save()
            return redirect('student_list')
    else:
        form = StudentCreationForm(instance=student.user, initial={'group': student.group})
    return render(request, 'journal/form.html', {'form': form, 'title': f'Redaktə: {student.user.get_full_name()}'})

@login_required
def edit_teacher(request, teacher_id):
    if not request.user.is_admin():
        return redirect('home')
    teacher = get_object_or_404(TeacherProfile, id=teacher_id)
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST, instance=teacher.user)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherCreationForm(instance=teacher.user)
    return render(request, 'journal/form.html', {'form': form, 'title': f'Redaktə: {teacher.user.get_full_name()}'})


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher():
        return redirect('home')
    try:
        teacher = request.user.teacher_profile
    except TeacherProfile.DoesNotExist:
        return redirect('home') # Should not happen if created correctly
        
    # Group subjects by Group
    dashboard_data = []
    teacher_groups = teacher.groups.all()
    teacher_subjects = teacher.subjects.all()
    
    for group in teacher_groups:
        dashboard_data.append({
            'group': group,
            'subjects': teacher_subjects
        })

    context = {
        'dashboard_data': dashboard_data,
    }
    return render(request, 'journal/teacher_dashboard.html', context)

@login_required
def grading_view(request, group_id, subject_id):
    if not request.user.is_teacher():
        return redirect('home')
    
    teacher = request.user.teacher_profile
    group = get_object_or_404(Group, id=group_id)
    subject = get_object_or_404(Subject, id=subject_id)
    
    # Simple check, can be more robust
    if subject not in teacher.subjects.all() or group not in teacher.groups.all():
        return redirect('teacher_dashboard')
    
    students = StudentProfile.objects.filter(group=group)
    
    if request.method == 'POST':
        for student in students:
            midterm = request.POST.get(f'midterm_{student.id}')
            presentation = request.POST.get(f'presentation_{student.id}')
            activity = request.POST.get(f'activity_{student.id}')
            final = request.POST.get(f'final_{student.id}')
            
            grade, created = Grade.objects.get_or_create(student=student, subject=subject)
            grade.midterm = int(midterm) if midterm else 0
            grade.presentation = int(presentation) if presentation else 0
            grade.activity = int(activity) if activity else 0
            grade.final = int(final) if final else 0
            grade.save()
        return redirect('grading_view', group_id=group.id, subject_id=subject.id)
        
    grades = Grade.objects.filter(student__in=students, subject=subject)
    grade_dict = {grade.student.id: grade for grade in grades}
    
    student_data = []
    chart_labels = []
    chart_data = []
    total_score_sum = 0
    graded_count = 0

    for student in students:
        grade = grade_dict.get(student.id)
        total = grade.calculate_total() if grade else 0
        
        student_data.append({
            'student': student,
            'grade': grade
        })
        
        chart_labels.append(student.user.get_full_name())
        chart_data.append(total)
        
        if grade:
            total_score_sum += total
            graded_count += 1
            
    group_average = round(total_score_sum / graded_count, 1) if graded_count > 0 else 0
        
    context = {
        'group': group,
        'subject': subject,
        'student_data': student_data,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'group_average': group_average,
    }
    return render(request, 'journal/grading.html', context)


@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return redirect('home')
    
    try:
        student = request.user.student_profile
    except StudentProfile.DoesNotExist:
        return redirect('home')
        
    grades = Grade.objects.filter(student=student)
    
    # Data for charts
    labels = [g.subject.name for g in grades]
    student_scores = [g.calculate_total() for g in grades]
    
    # Calculate averages for comparison
    averages = []
    for g in grades:
        all_grades = Grade.objects.filter(subject=g.subject)
        if all_grades.exists():
            total_sum = sum([grade.calculate_total() for grade in all_grades])
            avg_score = total_sum / all_grades.count()
        else:
            avg_score = 0
        averages.append(round(avg_score, 1))

    context = {
        'grades': grades,
        'labels': labels,
        'student_scores': student_scores,
        'averages': averages,
    }
    return render(request, 'journal/student_dashboard.html', context)

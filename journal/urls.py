from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-student/', views.create_student, name='create_student'),
    path('create-teacher/', views.create_teacher, name='create_teacher'),
    path('create-subject/', views.create_subject, name='create_subject'),
    path('create-group/', views.create_group, name='create_group'),
    path('assign-teacher/<int:teacher_id>/', views.assign_teacher, name='assign_teacher'),
    path('teacher-list/', views.teacher_list, name='teacher_list'),
    path('student-list/', views.student_list, name='student_list'),
    path('subject-list/', views.subject_list, name='subject_list'),
    path('group-list/', views.group_list, name='group_list'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('edit-teacher/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),
    
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('grading/<int:group_id>/<int:subject_id>/', views.grading_view, name='grading_view'),
    
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
]

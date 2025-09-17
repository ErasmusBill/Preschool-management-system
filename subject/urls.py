from django.urls import path, re_path
from . import views

app_name = "subject"

urlpatterns = [
    path('add/', views.add_subject, name='add-subject'),
    path('edit/<uuid:subject_id>/', views.edit_subject, name='edit-subject'),  
    path('delete/<uuid:subject_id>/', views.delete_subject, name='delete-subject'),  
    path('list/', views.list_all_subject, name='list-subject'),
    path("student-subject/<int:student_id>/",views.list_subject_by_student,name="student-subject"),
    path("register-subject/<int:subject_id>/",views.register_subject,name='register-subject')
]
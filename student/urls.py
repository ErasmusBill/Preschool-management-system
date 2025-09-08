from django.urls import path
from . import views

app_name = "student"

urlpatterns = [
    path('add/', views.add_student, name='add-student'),
    path('list/', views.student_list, name='student-list'),
    path('edit/<int:student_id>/', views.edit_student, name='edit-student'),
    path('detail/<int:student_id>/', views.student_detail, name='student-detail'),
    path('delete/<int:student_id>/', views.delete_student, name='delete-student'),
]
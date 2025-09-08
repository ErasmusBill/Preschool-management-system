from django.urls import path
from . import views

app_name = "teacher"

urlpatterns = [
    path('add/', views.add_teacher, name='add-teacher'),
    path('list/', views.list_all_teachers, name='list-teachers'),
    path('detail/<int:teacher_id>/', views.teacher_detail, name='teacher-detail'),
    path('edit/<int:teacher_id>/', views.edit_teacher, name='edit-teacher'),
    path('delete/<int:teacher_id>/', views.delete_teacher, name='delete-teacher'),
]
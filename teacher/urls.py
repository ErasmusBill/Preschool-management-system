from django.urls import path
from . import views

app_name = "teacher"

urlpatterns = [
    path('add/', views.add_teacher, name='add-teacher'),
    path('list/', views.list_all_teachers, name='list-teachers'),
    path('detail/<int:teacher_id>/', views.teacher_detail, name='teacher-detail'),
    path('edit/<int:teacher_id>/', views.edit_teacher, name='edit-teacher'),
    path('delete/<int:teacher_id>/', views.delete_teacher, name='delete-teacher'),
    path("add-assignment/", views.add_assignment, name="add-assignment"),
    #Assigments urls
    path("edit-assignment/<int:assignment_id>/", views.edit_assignment, name="edit-assignment"),
    path("delete-assignment/<int:assignment_id>/", views.delete_assignment, name="delete-assignment"),
    path("list-assignments/<int:teacher_id>/", views.list_assignments, name="list-assignments"),
    path("assignment-detail/<int:assignment_id>/", views.assignment_detail, name="assignment-detail"),
]
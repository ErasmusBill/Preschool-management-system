from django.urls import path
from . import views

app_name = "student"

urlpatterns = [
    path('add/', views.add_student, name='add-student'),
    path('list/', views.student_list, name='student-list'),
    path('edit/<int:student_id>/', views.edit_student, name='edit-student'),
    path('detail/<int:student_id>/', views.student_detail, name='student-detail'),
    path('delete/<int:student_id>/', views.delete_student, name='delete-student'),
    path('list_student_subject/<int:student_id>/',views.list_subject_related_to_student, name="list_student_subject"),
    path('view-assignments/<int:student_id>/',views.view_student_assignment,name="view-assignments"),
    
]
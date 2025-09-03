from django.urls import path


from . import views

app_name = 'student'

urlpatterns = [
   path('add-student/', views.add_student, name='add-student'),
   path('student-list/', views.student_list, name='student-list'),
   path('edit-student/<int:student_id>/', views.edit_student, name='edit-student'),
   path('student-detail/<int:student_id>/', views.student_detail, name='student-detail'),
   path('delete-student/<str:student_id>/',views.delete_student, name="delete-student"),
]
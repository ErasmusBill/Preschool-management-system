from django.urls import path
from . import views

app_name = "subject"

urlpatterns = [
    path('add/', views.add_subject, name='add-subject'),
    path('edit/<int:subject_id>/', views.edit_subject, name='edit-subject'),
    path('delete/<int:subject_id>/', views.delete_subject, name='delete-subject'),
    path('list/', views.list_all_subject, name='list-subject'),
]
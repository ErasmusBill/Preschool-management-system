from django.urls import path
from . import views

app_name = "department"

urlpatterns = [
    path('add/', views.add_department, name='add-department'),
    path('edit/<uuid:department_id>/', views.edit_department, name='edit-department'),
    path('list/', views.list_department, name='list-department'),
    path('delete/<uuid:department_id>/', views.delete_department, name='delete-department'),
    path('detail/<uuid:department_id>/', views.department_detail, name='department-detail'),
]
from django.urls import path
from . import views

app_name = "school"

urlpatterns = [
    path('index/', views.index, name='index'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/student/<int:student_id>/", views.view_student_dashboard, name="view-student-dashboard"),
    
    path('mark-notification-as-read/<uuid:notification_id>/', views.mark_notification_as_read, name='mark-notification-as-read'),
    path('clear-all-notifications/', views.clear_all_notifications, name='clear-all-notifications'),
]
from django import views
from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path("add-fees/",views.add_fees, name="add-fees"),
    path("list-fees/",views.list_student_fees, name="list-fees")
]

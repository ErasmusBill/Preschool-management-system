from django.urls import path
from . import views

app_name = 'home_auth'

urlpatterns = [
    path('register/', views.signup_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset-password/<str:token>/', views.reset_password_view, name='reset-password'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
 
]

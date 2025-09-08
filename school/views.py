from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification
from student.models import Student
from teacher.models import Teacher


def index(request):
    return render(request, 'school/index.html')


def create_notification(user, message):
    if user.is_authenticated:
        Notification.objects.create(user=user, message=message)


@login_required(login_url='home_auth:login') 
def mark_notification_as_read(request, notification_id):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()


@login_required(login_url='home_auth:login')
def clear_all_notifications(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()


@login_required(login_url='home_auth:login')
def dashboard(request):
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()

  
    recent_students = Student.objects.all().order_by('-joining_date')[:5]
    recent_teachers = Teacher.objects.all().order_by('-joining_date')[:5]

    # Handle notifications only for logged-in users
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notifications_count = unread_notifications.count()

    context = {
        'unread_notifications': unread_notifications,
        'unread_notifications_count': unread_notifications_count,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'recent_students': recent_students,
        'recent_teachers': recent_teachers,
    }

    # Role-based dashboards
    if hasattr(request.user, "role"):
        if request.user.role == 'admin':
            return render(request, 'school/admin-dashboard.html', context)
        elif request.user.role == 'teacher':
            return render(request, 'school/teacher-dashboard.html', context)
        elif request.user.role == 'student':
            return render(request, 'school/student-dashboard.html', context)

    # Fallback if no role is assigned
    messages.error(request, "Your account does not have a valid role.")
    return redirect("index")

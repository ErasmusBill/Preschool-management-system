from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification
from student.models import Student
from teacher.models import Teacher

@login_required(login_url='home_auth:login') 
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
def dashboard(request, student_id=None):
    """Main dashboard - redirects based on user role"""
    
    if request.user.role == 'admin':
        return admin_dashboard(request)
    elif request.user.role == 'teacher':
        return teacher_dashboard(request)
    elif request.user.role == 'student':
        return student_dashboard(request)
    else:
        messages.error(request, "Your account does not have a valid role.")
        return redirect("home_auth:login")

@login_required(login_url='home_auth:login')
def admin_dashboard(request):
    """Admin dashboard with student selection"""
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    
    recent_students = Student.objects.all().order_by('-joining_date')[:5]
    recent_teachers = Teacher.objects.all().order_by('-joining_date')[:5]
    
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
    
    return render(request, 'school/index.html', context)

@login_required(login_url='home_auth:login')
def teacher_dashboard(request):
    """Teacher dashboard"""
    # Get the teacher object for the current user
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        teacher = None
    
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    
    recent_students = Student.objects.all().order_by('-joining_date')[:5]
    recent_teachers = Teacher.objects.all().order_by('-joining_date')[:5]
    
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notifications_count = unread_notifications.count()
    
    context = {
        'unread_notifications': unread_notifications,
        'unread_notifications_count': unread_notifications_count,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'recent_students': recent_students,
        'recent_teachers': recent_teachers,
        'teacher': teacher,
    }
    
    return render(request, 'school/teacher-dashboard.html', context)

@login_required(login_url='home_auth:login')
def student_dashboard(request):
    """Student dashboard - shows their own data"""
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect("home_auth:login")
    
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notifications_count = unread_notifications.count()
    
    context = {
        'unread_notifications': unread_notifications,
        'unread_notifications_count': unread_notifications_count,
        'student_count': student_count,
        'teacher_count': teacher_count,
        'student': student,
    }
    
    return render(request, 'school/student-dashboard.html', context)

@login_required(login_url='home_auth:login')
def view_student_dashboard(request):
    """Student dashboard - shows their own data"""
    try:
        student = request.user.student_profile  # Using related_name
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect("home_auth:login")
    
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notifications_count = unread_notifications.count()
    
    context = {
        'unread_notifications': unread_notifications,
        'unread_notifications_count': unread_notifications_count,
        'student': student,
    }
    
    return render(request, 'school/student-dashboard.html', context)
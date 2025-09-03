from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from .models import Notification

# Create your views here.

def index(request):
    return render(request, 'school/index.html')

def create_notification(user, message):
    Notification.objects.create(user=user, message=message)
    
    
def mark_notification_as_read(request, notification_id):
    if request.method == 'POST':
        notification = Notification.objects.filter(user=request.user,is_read=False)
        notification.update(is_read=True)
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()

def clear_all_notifications(request):
    if request.method == 'POST':
        notifications = Notification.objects.filter(user=request.user,is_read=False)
        notifications.delete()
        return JsonResponse({'status': 'success'})
    return HttpResponseForbidden()

def dashboard(request):
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
    unread_notifications_count = unread_notifications.count()
    context = {
        'unread_notifications': unread_notifications,
        'unread_notifications_count': unread_notifications_count,
    }
    if request.user.role == 'admin':
        return render(request, 'school/admin-dashboard.html', context)
    elif request.user.role == 'teacher':
        return render(request, 'school/teacher-dashboard.html', context)
    elif request.user.role == 'student':
        return render(request, 'school/student-dashboard.html', context)
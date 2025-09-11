from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import os
from .forms import AssignmentForm
from .models import Assignment, Subject, Teacher, Department
from home_auth.models import CustomUser
from teacher.models import Assignment, Subject
from django.utils import timezone

def add_teacher(request):
    """Add a new teacher with a linked CustomUser account and profile image."""
    if not request.user.is_authenticated or not request.user.role != "admin":
        messages.error(request, "You don't have permission to perform this action")
        return redirect("teacher:add-teacher")
    
    departments = Department.objects.all()

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")

        department_id = request.POST.get("department")
        date_of_birth = request.POST.get("date_of_birth")
        gender = request.POST.get("gender")
        mobile = request.POST.get("mobile")
        qualification = request.POST.get("qualification")
        experience = request.POST.get("experience")
        joining_date = request.POST.get("joining_date")
        address = request.POST.get("address")
        city = request.POST.get("city")
        zipcode = request.POST.get("zipcode")
        country = request.POST.get("country")

       
        image = request.FILES.get("image")

        required_fields = [
            first_name, last_name, email, password, department_id,
            date_of_birth, gender, mobile, qualification, experience,
            joining_date, address, city, zipcode, country
        ]
        if not all(required_fields):
            messages.error(request, "All fields are required.")
            return render(request, "teacher/add-teacher.html", {
                "departments": departments,
                "form_data": request.POST
            })

        if password != repeat_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "teacher/add-teacher.html", {
                "departments": departments,
                "form_data": request.POST
            })

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "teacher/add-teacher.html", {
                "departments": departments,
                "form_data": request.POST
            })

        try:
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role="teacher",
                is_authorized=True
            )

            department = get_object_or_404(Department, id=department_id)
            Teacher.objects.create(
                user=user,
                department_id=department,
                date_of_birth=date_of_birth,
                gender=gender,
                mobile=mobile,
                qualification=qualification,
                experience=experience,
                joining_date=joining_date,
                address=address,
                city=city,
                zipcode=zipcode,
                country=country,
                image=image,  
            )

            subject = "Your Teacher Account Credentials"
            message = (
                f"Dear {first_name} {last_name},\n\n"
                "Your account has been created successfully.\n\n"
                f"Email: {email}\n"
                f"Password: {password}\n\n"
                "You can log in to the system using these credentials.\n\n"
                "Best regards,\nSchool Administration"
            )
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            except Exception as e:
                messages.warning(request, f"Teacher created, but email could not be sent. Error: {e}")

            messages.success(request, f"Teacher {first_name} {last_name} added successfully.")
            return redirect("teacher:list-teachers")

        except Exception as e:
            messages.error(request, f"Error creating teacher: {str(e)}")
            return render(request, "teacher/add-teacher.html", {
                "departments": departments,
                "form_data": request.POST
            })

    return render(request, "teacher/add-teacher.html", {"departments": departments})


def list_all_teachers(request):
    if not request.user.is_authenticated or not request.user.role != "admin":
        messages.error(request, "You don't have permission to perform this action")
        return redirect("teacher:list-teachers")
    
    """List all teachers with related user and department info."""
    teachers = Teacher.objects.select_related("user", "department_id").all()
    return render(request, "teacher/teachers.html", {"teachers": teachers})


def teacher_detail(request, teacher_id):
    """Show details of a single teacher."""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, "teacher/teacher-details.html", {"teacher": teacher})


def edit_teacher(request, teacher_id):
    if not request.user.is_authenticated or not request.user.role != "teacher" or not request.user.role != "admin":
        messages.error(request, "You don't have permission to perform this action")
        return redirect("teacher:teacher-list")
    
    """Edit teacher, associated user account, and profile image."""
    teacher = get_object_or_404(Teacher, id=teacher_id)
    user = teacher.user
    departments = Department.objects.all()

    if request.method == "POST":
        # update user
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        password = request.POST.get("password")
        if password:
            user.set_password(password)
        user.save()

       
        department_id = request.POST.get("department")
        if department_id:
            teacher.department_id = get_object_or_404(Department, id=department_id)

        teacher.date_of_birth = request.POST.get("date_of_birth")
        teacher.gender = request.POST.get("gender")
        teacher.mobile = request.POST.get("mobile")
        teacher.qualification = request.POST.get("qualification")
        teacher.experience = request.POST.get("experience")
        teacher.joining_date = request.POST.get("joining_date")
        teacher.address = request.POST.get("address")
        teacher.city = request.POST.get("city")
        teacher.zipcode = request.POST.get("zipcode")
        teacher.country = request.POST.get("country")

       
        new_image = request.FILES.get("image")
        if new_image:
            teacher.image = new_image

        teacher.save()

        messages.success(request, f"Teacher {user.first_name} {user.last_name} updated successfully.")
        return redirect("teacher:list-teachers")

    return render(request, "teacher/edit-teacher.html", {
        "teacher": teacher,
        "departments": departments
    })


def delete_teacher(request, teacher_id):
    """Delete teacher and linked user account, remove image file if exists."""
    if not request.user.is_authenticated or not request.user.role != "admin":
        messages.error(request, "You don't have permission to perform this action")
        return redirect("teacher:list-teachers")
    
    teacher = get_object_or_404(Teacher, id=teacher_id)
    user = teacher.user
    teacher_name = f"{user.first_name} {user.last_name}"

 
    if teacher.image and hasattr(teacher.image, "path"):
        if os.path.exists(teacher.image.path):
            os.remove(teacher.image.path)

    teacher.delete()
    user.delete()

    messages.success(request, f"Teacher {teacher_name} deleted successfully.")
    return redirect("teacher:list-teachers")

def add_assignment(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page.")
        return redirect("home_auth:login")
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, "You are not a registered teacher")
        return redirect("school:dashboard")

    # Optional: Check if teacher has subjects
    if not teacher.subject_set.exists():
        messages.error(request, "You have no subjects assigned. Please contact administration.")
        return redirect("school:dashboard")

    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        form.fields["subject"].queryset = teacher.subject_set.all() 

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = teacher 
            assignment.save()  

            messages.success(request, "Assignment added successfully.")
            return redirect("teacher:list-assignments", args=[str(teacher.id)])
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)  
    else:
        form = AssignmentForm()
        form.fields["subject"].queryset = teacher.subject_set.all()

    return render(request, "teacher/add-assignment.html", {"form": form, "teacher": teacher})

def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    try:
        current_teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, "You are not a teacher.")
        return redirect(reverse("home_auth:login"))

    if assignment.teacher != current_teacher:
        messages.error(request, "You do not have permission to edit this assignment.")
        return redirect(reverse("teacher:list-assignments", args=[current_teacher.id]))

    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            assignment = form.save()
            messages.success(request, "Assignment successfully updated.")
            return redirect(reverse("teacher:assignment-detail", args=[assignment.id]))
    else:
        form = AssignmentForm(instance=assignment)

    # ✅ Make sure to pass 'teacher' to context so template can use {% url 'teacher:list-assignments' teacher.id %}
    return render(request, "teacher/edit-assignment.html", {
        "form": form,
        "assignment": assignment,
        "teacher": current_teacher  
    })

def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
  
    if not assignment.teacher:
        messages.error(request, "This assignment is not linked to a valid teacher.")
        return redirect("school:dashboard")
    
    teacher = assignment.teacher
    assignment.delete()
    messages.success(request, "Assignment successfully deleted")
    
    return redirect("teacher:list-assignments", teacher_id=teacher.id)


def list_assignments(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    assignments = Assignment.objects.filter(teacher=teacher)
    subjects = Subject.objects.all()
    

    now = timezone.now()
    context = {
        'assignments': assignments,
        'teacher': teacher,
        'subjects': subjects,
        'active_assignments_count': assignments.filter(start_time__lte=now, due_time__gte=now).count(),
        'upcoming_assignments_count': assignments.filter(start_time__gt=now).count(),
        'overdue_assignments_count': assignments.filter(due_time__lt=now).count(),
    }
    return render(request, 'teacher/list-assignments.html', context)

def assignment_detail(request,assignment_id):
    assignment = get_object_or_404(Assignment,id=assignment_id)
    return render(request,"teacher/assignment-detail.html",{"assignment":assignment})
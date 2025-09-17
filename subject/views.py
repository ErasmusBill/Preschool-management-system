from django.shortcuts import render, redirect, get_object_or_404
from student.models import Student
from teacher.models import Enrollment, Subject, Teacher
from django.contrib import messages
from .forms import RegisterForm
# Create your views here.

def add_subject(request):
    if not request.user.is_authenticated or request.user.role != "admin":
        messages.error(request, "You are not authorized to perform this action")
        return redirect("school:index")

    teachers = Teacher.objects.all()

    if request.method == "POST":
        subject_name = request.POST.get("subject_name").strip()
        grade = request.POST.get("grade").strip()
        teacher_id = request.POST.get("teacher_id")

        if not subject_name or not grade or not teacher_id:
            messages.error(request, "All fields are required.")
            return render(request, "subject/add-subject.html", {"teachers": teachers})

        try:
            teacher = get_object_or_404(Teacher, id=teacher_id)
            subject = Subject.objects.create(
                name=subject_name,
                grade=grade,
                teacher=teacher  
            )
            messages.success(request, f"{subject_name} added successfully")
            return redirect("subject:subject-list")
        except Exception as e:
            messages.error(request, f"Error creating subject: {str(e)}")
            return render(request, "subject/add-subject.html", {"teachers": teachers})

    return render(request, "subject/add-subject.html", {"teachers": teachers})

def edit_subject(request, subject_id):
    if not request.user.is_authenticated or request.user.role != "admin":
        messages.error(request, "You are not authorized to perform this action")
        return redirect("school:home")

    subject = get_object_or_404(Subject, id=subject_id)
    teachers = Teacher.objects.all()

    if request.method == "POST":
        subject.name = request.POST.get("subject_name").strip()
        subject.grade = request.POST.get("grade").strip()
        teacher_id = request.POST.get("teacher_id")

        if not subject.name or not subject.grade or not teacher_id:
            messages.error(request, "All fields are required.")
            return render(request, "subject/edit-subject.html", {"subject": subject, "teachers": teachers})

        try:
            subject.teacher = get_object_or_404(Teacher, id=teacher_id)
            subject.save()
            messages.success(request, f"{subject.name} updated successfully")
            return redirect("subject:list-subject")
        except Exception as e:
            messages.error(request, f"Error updating subject: {str(e)}")
            return render(request, "subject/edit-subject.html", {"subject": subject, "teachers": teachers})

    return render(request, "subject/edit-subject.html", {"subject": subject, "teachers": teachers})

def list_all_subject(request):
    if not request.user.is_authenticated or request.user.role != "admin":
        messages.error(request, "You are not authorized to perform this action")
        return redirect("school:home")

    subjects = Subject.objects.all()
    return render(request, "subject/subjects.html", {"subjects": subjects})


def delete_subject(request, subject_id):
    if not request.user.is_authenticated or request.user.role != "admin":
        messages.error(request, "You are not authorized to perform this action")
        return redirect("school:home")

    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, "Subject successfully deleted")
    return redirect("subject:list-subject")


def list_subject_by_student(request, student_id):
    """Get subjects enrolled by a student."""
    student = get_object_or_404(Student, id=student_id)

 
    subjects = Subject.objects.filter(enrollment__student=student).distinct()

    if not subjects.exists():
        messages.error(request, "Please go to the account office to activate your account")
        return redirect("school:dashboard")

    return render(
        request,
        "subject/student-subject.html",
        {"subjects": subjects, "student": student}
    )

def register_subject(request, student_id):
    if not request.user.is_authenticated or request.user.role == "student":
        messages.error(request, "You are not authorized to perform this action")
        return redirect("home_auth:login")

    student = get_object_or_404(Student, id=student_id)
    grade_level = student.student_class
    subjects = Subject.objects.filter(grade_level=grade_level)

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            enrollment = register_form.save(commit=False)
            enrollment.student = student
            enrollment.save()
            messages.success(request, "Subject registered successfully.")
            return redirect("subject:subject-list")  
    else:
        register_form = RegisterForm()

    return render(request,"student/register-subject.html",{"register_form": register_form, "subjects": subjects})
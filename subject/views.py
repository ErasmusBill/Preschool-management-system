from django.shortcuts import render, redirect, get_object_or_404
from teacher.models import Subject, Teacher
from django.contrib import messages

# Create your views here.

def add_subject(request):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You are not authorized to perform this action")
    #     return redirect("school:home")

    teachers = Teacher.objects.all()

    if request.method == "POST":
        subject_name = request.POST.get("subject_name")
        grade = request.POST.get("grade")
        teacher_id = request.POST.get("teacher_id")

        teacher = get_object_or_404(Teacher, id=teacher_id)

        subject = Subject.objects.create(
            name=subject_name,
            grade=grade,
            teacher_id=teacher
        )
        messages.success(request, f"{subject_name} added successfully")
        return redirect("subject:subject-list")

    return render(request, "subject/add-subject.html", {"teachers": teachers})


def edit_subject(request, subject_id):
    if not request.user.is_authenticated or request.user.role != "admin":
        messages.error(request, "You are not authorized to perform this action")
        return redirect("school:home")

    subject = get_object_or_404(Subject, id=subject_id)
    teachers = Teacher.objects.all()

    if request.method == "POST":
        subject.name = request.POST.get("subject_name")
        subject.grade = request.POST.get("grade")
        teacher_id = request.POST.get("teacher_id")
        subject.teacher_id = get_object_or_404(Teacher, id=teacher_id)

        subject.save()
        messages.success(request, f"{subject.name} successfully updated")
        return redirect("subject:subject-list")

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
    return redirect("subject:subject-list")

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Student,Parent
from school.views import create_notification


from datetime import datetime


# Create your views here.

def add_student(request):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You are not authorized to perform this action")
    #     return redirect("school:index")

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        religion = request.POST.get('religion')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')
        mobile_number = request.POST.get('mobile_number')
        joining_date = request.POST.get('joining_date')

        # parent/guardian information
        father_name = request.POST.get('father_name')
        father_phone = request.POST.get('father_phone')
        father_occupation = request.POST.get('father_occupation')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_phone = request.POST.get('mother_phone')
        mother_occupation = request.POST.get('mother_occupation')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

       
        if not all([
            first_name, last_name, student_id, gender, date_of_birth,
            student_class, admission_number, section, student_image,
            mobile_number, father_name, father_phone, father_occupation,
            father_email, mother_name, mother_phone, mother_occupation,
            mother_email, present_address, permanent_address, joining_date
        ]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('student:add-student')

        # create parent
        parent = Parent.objects.create(
            father_name=father_name,
            father_phone=father_phone,
            father_occupation=father_occupation,
            father_email=father_email,
            mother_name=mother_name,
            mother_phone=mother_phone,
            mother_occupation=mother_occupation,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address
        )

        # create student
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            student_class=student_class,
            religion=religion,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            mobile_number=mobile_number,
            joining_date=joining_date,
            parent=parent
        )


        create_notification(request.user, f'New student {first_name} {last_name} added.')

        messages.success(request, f'Student {first_name} {last_name} added successfully.')
        return redirect('student:student-list')

    return render(request, 'student/add-student.html')


def student_list(request):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You are not authorized to perform this action")
    #     return redirect("school:index")

    students = Student.objects.all()
    return render(request, 'student/students.html', {'students': students})


def edit_student(request, student_id):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You are not authorized to perform this action")
    #     return redirect("school:index")

    student = get_object_or_404(Student, student_id=student_id)
    parent = getattr(student, 'parent', None)

    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student_id = request.POST.get('student_id')
        student.gender = request.POST.get('gender')
        student.student_class = request.POST.get('student_class')
        student.religion = request.POST.get('religion')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')
        student.mobile_number = request.POST.get('mobile_number')

     
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            student.date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()

        joining_date = request.POST.get('joining_date')
        if joining_date:
            student.joining_date = datetime.strptime(joining_date, "%Y-%m-%d").date()

        student_image = request.FILES.get('student_image')
        if student_image:
            student.student_image = student_image

   
        if parent:
            parent.father_name = request.POST.get('father_name')
            parent.father_phone = request.POST.get('father_phone')
            parent.father_occupation = request.POST.get('father_occupation')
            parent.father_email = request.POST.get('father_email')
            parent.mother_name = request.POST.get('mother_name')
            parent.mother_phone = request.POST.get('mother_phone')
            parent.mother_occupation = request.POST.get('mother_occupation')
            parent.mother_email = request.POST.get('mother_email')
            parent.present_address = request.POST.get('present_address')
            parent.permanent_address = request.POST.get('permanent_address')
            parent.save()

        student.save()

        create_notification(request.user, f'Student {student.first_name} {student.last_name} updated.')

        messages.success(request, f"Student {student.first_name} {student.last_name} updated successfully.")
        return redirect('student:student-list')

    return render(request, 'student/edit-student.html', {"student": student, "parent": parent})


def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'student/student-details.html', {'student': student})


def delete_student(request, student_id):
    if not request.user.is_authenticated or request.user.role != "admin":
        messages.error(request, "You are not authorized to perform this action")
        return redirect("school:index")

    if request.method == "POST":
        student = get_object_or_404(Student, student_id=student_id)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()


        create_notification(request.user, f'Student {student_name} deleted.')

        messages.success(request, f'Student {student_name} deleted successfully.')
        return redirect('student:student-list')

    return HttpResponseForbidden()
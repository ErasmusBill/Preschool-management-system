from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

from .models import Student, Parent
from school.views import create_notification


def add_student(request):
    """
    Add a new student and parent information.
    Sends an email notification to parents after successful addition.
    """
    if not request.user.is_authenticated or request.user.role != 'admin':
        messages.error(request, "You don't have permission to perform this action")
        return redirect("student:student-list")
    if request.method == 'POST':
        # student account info
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        
        # student info
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

        # parent info
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

        # validate required fields
        if not all([
            email, password, first_name, last_name, student_id, gender, date_of_birth,
            student_class, admission_number, section, student_image,
            mobile_number, father_name, father_phone, father_occupation,
            father_email, mother_name, mother_phone, mother_occupation,
            mother_email, present_address, permanent_address, joining_date
        ]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('student:add-student')
            
        # validate password
        if password != repeat_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('student:add-student')
            
        # check if email already exists
        from home_auth.models import CustomUser
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('student:add-student')

        try:
            # create user account for student
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role="student",
                is_authorized=True
            )
            
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
                user=user,
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
            
            # notify admins (in-app notification)
            create_notification(request.user, f'New student {first_name} {last_name} added.')
            
            # send email to parents
            subject = "Your Student Account Credentials"
            message = (
                f"Dear {father_name} and {mother_name},\n\n"
                f"Your child {first_name} {last_name} has been successfully enrolled.\n\n"
                f"Student Portal Login:\n"
                f"Email: {email}\n"
                f"Password: {password}\n\n"
                f"Student Class: {student_class}\n"
                f"Section: {section}\n"
                f"Admission Number: {admission_number}\n"
                f"Joining Date: {joining_date}\n\n"
                "Thank you for choosing our school.\n\nBest regards,\nSchool Administration"
            )
            recipient_list = [father_email, mother_email]
            
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            except Exception as e:
                messages.warning(request, f"Student added, but email could not be sent. Error: {e}")
            
            messages.success(request, f'Student {first_name} {last_name} added successfully.')
            return redirect('student:student-list')
            
        except Exception as e:
            messages.error(request, f'Error creating student: {str(e)}')
            return redirect('student:add-student')

        # notify admins (in-app notification)
        create_notification(request.user, f'New student {first_name} {last_name} added.')

      
        subject = "New Student Enrollment Confirmation"
        message = (
            f"Dear {father_name} and {mother_name},\n\n"
            f"Your child {first_name} {last_name} has been successfully enrolled "
            f"in class {student_class}, section {section}.\n\n"
            f"Admission Number: {admission_number}\n"
            f"Joining Date: {joining_date}\n\n"
            "Thank you for choosing our school.\n\nBest regards,\nSchool Administration"
        )
        recipient_list = [father_email, mother_email]

        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        except Exception as e:
            messages.warning(request, f"Student added, but email could not be sent. Error: {e}")

        messages.success(request, f'Student {first_name} {last_name} added successfully.')
        return redirect('student:student-list')

    return render(request, 'student/add-student.html')


def student_list(request):
    """List all students."""
    if not request.user.is_authenticated or  request.user.role != 'admin':
        messages.error(request, "You don't have permission to perform this action")
        return redirect("student:add-student")  
    
    students = Student.objects.all()
    return render(request, 'student/students.html', {'students': students})


def edit_student(request, student_id):
    """Edit existing student and parent information."""
    if not request.user.is_authenticated or  request.user.role != 'admin':
        messages.error(request, "You don't have permission to perform this action")
        return redirect("student:student-list") 
    
    student = get_object_or_404(Student, student_id=student_id)
    parent = getattr(student, 'parent', None)

    if request.method == 'POST':
        # update student info
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student_id = request.POST.get('student_id')
        student.gender = request.POST.get('gender')
        student.student_class = request.POST.get('student_class')
        student.religion = request.POST.get('religion')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')
        student.mobile_number = request.POST.get('mobile_number')

        
        dob = request.POST.get('date_of_birth')
        if dob:
            student.date_of_birth = datetime.strptime(dob, "%Y-%m-%d").date()

        join_date = request.POST.get('joining_date')
        if join_date:
            student.joining_date = datetime.strptime(join_date, "%Y-%m-%d").date()

        
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
    """View detailed information about a student."""
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'student/student-details.html', {'student': student})


def delete_student(request, student_id):
    """Delete a student record."""
    if not request.user.is_authenticated or request.user.role != "admin":
        messages.error(request, "You are not authorized to perform this action")
        return redirect("student:student-list")

    if request.method == "POST":
        student = get_object_or_404(Student, student_id=student_id)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()

        create_notification(request.user, f'Student {student_name} deleted.')
        messages.success(request, f'Student {student_name} deleted successfully.')
        return redirect('student:student-list')

    return HttpResponseForbidden()

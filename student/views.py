from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from .models import Student, Parent
from home_auth.models import CustomUser
from school.views import create_notification
from teacher.models import Subject,Assignment,Grade

def add_student(request):
    """Add a new student and parent information with comprehensive validation."""
    # Authentication and authorization check
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to access this page.")
        return redirect("home_auth:login")
    
    if request.user.role != 'admin':
        messages.error(request, "You don't have permission to perform this action.")
        return redirect("school:dashboard")

    if request.method == 'POST':
        print("=" * 50)
        print("POST data received")
        print(f"POST: {dict(request.POST)}")
        print(f"FILES: {dict(request.FILES)}")

        # Extract all form data
        form_data = {
            # Student account info
            'email': request.POST.get('email', '').strip(),
            'password': request.POST.get('password', '').strip(),
            'repeat_password': request.POST.get('repeat_password', '').strip(),

            # Student personal info
            'first_name': request.POST.get('first_name', '').strip(),
            'last_name': request.POST.get('last_name', '').strip(),
            'student_id': request.POST.get('student_id', '').strip(),
            'gender': request.POST.get('gender', '').strip(),
            'date_of_birth': request.POST.get('date_of_birth', '').strip(),
            'student_class': request.POST.get('student_class', '').strip(),
            'religion': request.POST.get('religion', '').strip(),
            'admission_number': request.POST.get('admission_number', '').strip(),
            'section': request.POST.get('section', '').strip(),
            'mobile_number': request.POST.get('mobile_number', '').strip(),
            'joining_date': request.POST.get('joining_date', '').strip(),
            'student_image': request.FILES.get('student_image'),

            # Parent info
            'father_name': request.POST.get('father_name', '').strip(),
            'father_phone': request.POST.get('father_phone', '').strip(),
            'father_occupation': request.POST.get('father_occupation', '').strip(),
            'father_email': request.POST.get('father_email', '').strip(),
            'mother_name': request.POST.get('mother_name', '').strip(),
            'mother_phone': request.POST.get('mother_phone', '').strip(),
            'mother_occupation': request.POST.get('mother_occupation', '').strip(),
            'mother_email': request.POST.get('mother_email', '').strip(),
            'present_address': request.POST.get('present_address', '').strip(),
            'permanent_address': request.POST.get('permanent_address', '').strip(),
        }

        print(f"Extracted form_data: {form_data}")

        # Required fields validation
        required_fields = [
            'email', 'password', 'repeat_password', 'first_name', 'last_name',
            'student_id', 'gender', 'date_of_birth', 'student_class',
            'admission_number', 'section', 'mobile_number', 'joining_date',
            'father_name', 'father_phone', 'father_email', 'mother_name',
            'mother_phone', 'mother_email', 'present_address', 'permanent_address'
        ]

        missing_fields = [field for field in required_fields if not form_data[field]]
        if missing_fields:
            error_msg = f'Missing required fields: {", ".join(missing_fields)}'
            print(f"Validation error: {error_msg}")
            messages.error(request, error_msg)
            return render(request, 'student/add-student.html', {'form_data': form_data})

        # Password validation
        if form_data['password'] != form_data['repeat_password']:
            print("Validation error: Passwords do not match")
            messages.error(request, 'Passwords do not match.')
            return render(request, 'student/add-student.html', {'form_data': form_data})

        if len(form_data['password']) < 8:
            print("Validation error: Password too short")
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'student/add-student.html', {'form_data': form_data})

        # Email uniqueness check
        if CustomUser.objects.filter(email=form_data['email']).exists():
            print(f"Validation error: Email {form_data['email']} already exists")
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'student/add-student.html', {'form_data': form_data})

        # Student ID uniqueness check
        if Student.objects.filter(student_id=form_data['student_id']).exists():
            print(f"Validation error: Student ID {form_data['student_id']} already exists")
            messages.error(request, 'Student ID already exists. Please use a different ID.')
            return render(request, 'student/add-student.html', {'form_data': form_data})

        # Admission number uniqueness check
        if Student.objects.filter(admission_number=form_data['admission_number']).exists():
            print(f"Validation error: Admission number {form_data['admission_number']} already exists")
            messages.error(request, 'Admission number already exists. Please use a different number.')
            return render(request, 'student/add-student.html', {'form_data': form_data})

        # Date validation
        try:
            dob_date = datetime.strptime(form_data['date_of_birth'], "%Y-%m-%d").date()
            join_date = datetime.strptime(form_data['joining_date'], "%Y-%m-%d").date()
            
            if dob_date > datetime.now().date():
                print("Validation error: Date of birth in future")
                messages.error(request, 'Date of birth cannot be in the future.')
                return render(request, 'student/add-student.html', {'form_data': form_data})
            
            if join_date > datetime.now().date():
                print("Validation error: Joining date in future")
                messages.error(request, 'Joining date cannot be in the future.')
                return render(request, 'student/add-student.html', {'form_data': form_data})

        except ValueError as e:
            print(f"Date validation error: {e}")
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD format.')
            return render(request, 'student/add-student.html', {'form_data': form_data})

        # Create objects
        user = None
        parent = None
        student = None

        try:
            print("Attempting to create user...")
            # Create user account
            user = CustomUser.objects.create_user(
                username=form_data['email'],
                email=form_data['email'],
                password=form_data['password'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                role="student",
                is_authorized=True
            )
            print(f"✓ User created successfully: {user.id} - {user.email}")

            print("Attempting to create parent...")
            # Create parent information
            parent = Parent.objects.create(
                father_name=form_data['father_name'],
                father_phone=form_data['father_phone'],
                father_occupation=form_data['father_occupation'],
                father_email=form_data['father_email'],
                mother_name=form_data['mother_name'],
                mother_phone=form_data['mother_phone'],
                mother_occupation=form_data['mother_occupation'],
                mother_email=form_data['mother_email'],
                present_address=form_data['present_address'],
                permanent_address=form_data['permanent_address']
            )
            print(f"✓ Parent created successfully: {parent.id}")

            print("Attempting to create student...")
            # Create student profile
            student_data = {
                'user': user,
                'first_name': form_data['first_name'],
                'last_name': form_data['last_name'],
                'student_id': form_data['student_id'],
                'gender': form_data['gender'],
                'date_of_birth': dob_date,
                'student_class': form_data['student_class'],
                'religion': form_data['religion'],
                'admission_number': form_data['admission_number'],
                'section': form_data['section'],
                'mobile_number': form_data['mobile_number'],
                'joining_date': join_date,
                'parent': parent
            }
            
            if form_data['student_image']:
                student_data['student_image'] = form_data['student_image']
            
            student = Student.objects.create(**student_data)
            print(f"✓ Student created successfully: {student.id} - {student.student_id}")

            # Create notification
            create_notification(
                request.user, 
                f'New student {form_data["first_name"]} {form_data["last_name"]} added.'
            )
            print("✓ Notification created")

            # Send email to parents
            try:
                print("Attempting to send email...")
                subject = "New Student Enrollment Confirmation"
                message = (
                    f"Dear {form_data['father_name']} and {form_data['mother_name']},\n\n"
                    f"Your child {form_data['first_name']} {form_data['last_name']} has been successfully enrolled.\n\n"
                    f"Class: {form_data['student_class']}\n"
                    f"Section: {form_data['section']}\n"
                    f"Email: {form_data['email']}\n"
                    f"Password: {form_data['password']}\n"
                    f"Admission Number: {form_data['admission_number']}\n"
                    f"Joining Date: {form_data['joining_date']}\n\n"
                    "Thank you for choosing our school.\n\nBest regards,\nSchool Administration"
                )
                send_mail(
                    subject, 
                    message, 
                    settings.DEFAULT_FROM_EMAIL, 
                    [form_data['father_email'], form_data['mother_email']],
                    fail_silently=True
                )
                print("✓ Email sent successfully")
            except Exception as e:
                print(f"✗ Email sending failed: {e}")
                messages.warning(request, f"Student added, but email could not be sent: {e}")

            messages.success(
                request, 
                f'Student {form_data["first_name"]} {form_data["last_name"]} added successfully.'
            )
            
            print("✓ All operations completed successfully. Redirecting to student list.")
            # Redirect to student list
            return redirect('student:student-list')

        except IntegrityError as e:
            print(f"✗ IntegrityError: {e}")
            error_msg = 'Database integrity error. Please check if student ID or admission number already exists.'
            messages.error(request, error_msg)
            
            # Clean up any created objects
            if student:
                print("Deleting student due to error")
                student.delete()
            if parent:
                print("Deleting parent due to error")
                parent.delete()
            if user:
                print("Deleting user due to error")
                user.delete()
                
            return render(request, 'student/add-student.html', {'form_data': form_data})

        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'An unexpected error occurred: {str(e)}')
            
            # Clean up any created objects
            if student:
                print("Deleting student due to error")
                student.delete()
            if parent:
                print("Deleting parent due to error")
                parent.delete()
            if user:
                print("Deleting user due to error")
                user.delete()
                
            return render(request, 'student/add-student.html', {'form_data': form_data})

    # GET request - show empty form
    print("GET request - showing empty form")
    return render(request, 'student/add-student.html', {'form_data': {}})

def student_list(request):
    """List all students."""
    if not request.user.is_authenticated or request.user.role != 'admin':
        messages.error(request, "You don't have permission to perform this action")
        return redirect("home_auth:login")

    students = Student.objects.all()
    return render(request, 'student/students.html', {'students': students})


def edit_student(request, student_id):
    """Edit existing student and parent information."""
    if not request.user.is_authenticated or request.user.role != 'admin':
        messages.error(request, "You don't have permission to perform this action")
        return redirect("home_auth:login")

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

        # update parent info
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
        return redirect("home_auth:login")

    if request.method == "POST":
        student = get_object_or_404(Student, student_id=student_id)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()

        create_notification(request.user, f'Student {student_name} deleted.')
        messages.success(request, f'Student {student_name} deleted successfully.')
        return redirect('student:student-list')

    return HttpResponseForbidden()

def list_subject_related_to_student(request,student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Exception as e:
        messages.error(request,"Student Not Found")
        return redirect("school:dashboard")
    
    subjects = Subject.objects.filter(student=student)
    return render(request, "student/list-all-subject.html",{"subjects":subjects})


def view_student_assignment(request,student_id):
    
    student = get_object_or_404(Student,id=student_id)
    assignment_class = getattr(student,"student_class")
    assignments = Assignment.objects.filter(grade_level=assignment_class)
    return render(request,"student/student-assignments.html",{"assignments":assignments})


def view_results(request, student_id):
    """
    Display all grades for all subjects the student is enrolled in.
    """
    student = get_object_or_404(Student, id=student_id)

    # Get all grade records for this student
    results = (Grade.objects.filter(student=student).select_related("student_assignment__subject","student_assignment__teacher__user","enrollment__subject").order_by("enrollment__subject__name"))

    return render(request, "results/view_results.html", {"student": student,"results": results})
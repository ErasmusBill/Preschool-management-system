from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login
from .models import Teacher, Department, Subject
from home_auth.models import CustomUser

def add_teacher(request):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You don't have permission to perform this action")
    #     return redirect('school:index')  
    
    departments = Department.objects.all()
    
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Get teacher data
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
        
       
        required_fields = [
            first_name, last_name, email, password, department_id,
            date_of_birth, gender, mobile, qualification, experience,
            joining_date, address, city, zipcode, country
        ]
        
        if not all(required_fields):
            messages.error(request, "All fields are required")
            return render(request, "teacher/add-teacher.html", {
                "departments": departments,
                "form_data": request.POST
            })
        
        
        repeat_password = request.POST.get("repeat_password")
        if password != repeat_password:
            messages.error(request, "Passwords do not match")
            return render(request, "teacher/add-teacher.html", {
                "departments": departments,
                "form_data": request.POST
            })
        
        try:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return render(request, "teacher/add-teacher.html", {
                    "departments": departments,
                    "form_data": request.POST
                })
           
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='teacher',
                is_authorized=True
            )
            
            department = get_object_or_404(Department, id=department_id)
            
         
            teacher = Teacher.objects.create(
                user=user,
                department=department,
                date_of_birth=date_of_birth,
                gender=gender,
                mobile=mobile,
                qualification=qualification,
                experience=experience,
                joining_date=joining_date,
                address=address,
                city=city,
                zipcode=zipcode,
                country=country
            )
            
            messages.success(request, f"Teacher {first_name} {last_name} added successfully")
            return redirect("teacher:add-teacher")
            
        except Exception as e:
            messages.error(request, f"Error creating teacher: {str(e)}")
            return render(request, "teacher/add-teacher.html", {
                "departments": departments,
                "form_data": request.POST
            })
    
  
    return render(request, "teacher/add-teacher.html", {"departments": departments})

def list_all_teachers(request):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request,"You don't have permission to perform this action")
    #     return redirect('school:index')
    
    teachers = Teacher.objects.select_related("user", "department_id").all()
    return render(request, "teacher/teachers.html", {"teachers": teachers})

def teacher_detail(request, teacher_id):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request,"You don't have permission to perform this action")
    #     return redirect('school:index')
    
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, "teacher/teachers-details.html", {"teacher": teacher})

def edit_teacher(request, teacher_id):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You don't have permission to perform this action")
    #     return redirect('school:index')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    user = teacher.user

    if request.method == "POST":
        if user:
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            password = request.POST.get("password")
            if password:
                user.set_password(password)
            user.save()

      
        department_id = request.POST.get("department")
        if department_id:
            teacher.department_id = Department.objects.get(id=department_id)

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
        teacher.save()

        messages.success(request, f"Teacher {user.first_name} {user.last_name} updated successfully.")
        return redirect('teacher:list-teachers')

    return render(request, "teacher/edit-teacher.html", {"teacher": teacher})


def delete_teacher(request, teacher_id):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You don't have permission to perform this action")
    #     return redirect('school:index')
    
    teacher = get_object_or_404(Teacher, id=teacher_id)
    user = teacher.user
    
  
    teacher_name = f"{user.first_name} {user.last_name}"
    teacher.delete()
    user.delete()
    
    messages.success(request, f"Teacher {teacher_name} successfully deleted")
    return redirect("teacher:teacher-list")
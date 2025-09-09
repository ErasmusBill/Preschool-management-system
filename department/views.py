from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from teacher.models import Department


def add_department(request):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You don't have permission to perform this action")
    #     return redirect("school:index")

    if request.method == "POST":
        head_of_department = request.POST.get("head_of_department")
        department_name = request.POST.get("department_name")
        number_of_student = request.POST.get("number_of_student")
        department_start_date = request.POST.get("department_start_date")

        if not all([head_of_department, department_name, number_of_student, department_start_date]):
            messages.error(request, "All fields are required")
            return redirect("department:add-department")

        department = Department.objects.create(
            name=department_name,
            head_of_department=head_of_department,
            number_of_student=number_of_student,
            department_start_date=department_start_date,
        )
        messages.success(request, f"{department_name} department added successfully")
        return redirect("department:list-department")

    return render(request, "department/add-department.html")


def edit_department(request, department_id):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You don't have permission to perform this action")
    #     return redirect("school:index")

    department = get_object_or_404(Department, pk=department_id)

    if request.method == "POST":
        department.head_of_department = request.POST.get("head_of_department")
        department.name = request.POST.get("department_name")
        department.number_of_student = request.POST.get("number_of_student")
        department.department_start_date = request.POST.get("department_start_date")

        department.save()
        messages.success(request, f"You have successfully updated {department.name}")
        return redirect("department:list-department")

    return render(request, "department/edit-department.html", {"department": department})


def list_department(request):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You don't have permission to perform this action")
    #     return redirect("school:index")

    department_list = Department.objects.all().order_by("name")  
    paginator = Paginator(department_list, 10) 

    page_number = request.GET.get("page")
    departments = paginator.get_page(page_number)

    return render(request, "department/departments.html", {"departments": departments})


def department_detail(request, department_id):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You don't have permission to perform this action")
    #     return redirect("school:index")

    department = get_object_or_404(Department, id=department_id)
    return render(request, "department/department-detail.html", {"department": department})


def delete_department(request, department_id):
    # if not request.user.is_authenticated or request.user.role != "admin":
    #     messages.error(request, "You don't have permission to perform this action")
    #     return redirect("school:index")

    department = get_object_or_404(Department, pk=department_id)
    department.delete()
    messages.success(request, f"{department.name} successfully deleted")
    return redirect("department:list-department")

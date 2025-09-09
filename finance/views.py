from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Fees
from student.models import Student


def add_fees(request):
    """
    Add fees for a student and send email notifications to parents.
    """
    students = Student.objects.all()
    
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        fee_type = request.POST.get("fee_type")
        amount = request.POST.get("amount")
        
       
        if not all([student_id, fee_type, amount]):
            messages.error(request, "All fields are required")
            return redirect("finance:home")
        
       
        student = get_object_or_404(Student, student_id=student_id)
        
     
        fee = Fees.objects.create(
            student=student,
            amount=amount,
            exams_type=fee_type
        )
        
        
        recipients = []
        if student.parent.father_email:
            recipients.append(student.parent.father_email)
        if student.parent.mother_email:
            recipients.append(student.parent.mother_email)
        
       
        if recipients:
            subject = "New Fee Added for Your Child"
            message = (
                f"Dear {student.parent.father_name} and {student.parent.mother_name},\n\n"
                f"A new fee has been recorded for your child {student.first_name} {student.last_name}:\n"
                f"Type: {fee_type}\n"
                f"Amount: {amount}\n\n"
                f"Thank you,\nSchool Administration"
            )
            
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipients)
                messages.success(request, "Fees added successfully and email sent to parents!")
            except Exception as e:
                messages.warning(request, f"Fees added but email could not be sent: {e}")
        else:
            messages.success(request, "Fees added successfully (no parent email found).")
        
        return redirect("finance:list-fees")
    
    context = {"students": students}
    return render(request, "finance/add-fees.html", context)


def list_student_fees(request, student_id=None):
    """
    List fees for a specific student or all students.
    """
    student = None
    if student_id:
        student = get_object_or_404(Student, student_id=student_id)
        fees = Fees.objects.filter(student=student)
    else:
        fees = Fees.objects.all()
    
    context = {
        "fees": fees,
        "student": student
    }
    return render(request, "finance/fees-collections.html", context)

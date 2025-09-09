from django.db import models
from home_auth.models import CustomUser

# Create your models here.

class Fees(models.Model):
    FEES_CHOICES = [
        ("class_test","Class_Test"),
        ("exams","Exams"),
        ("hostel","Hostel"),
        ("transport","Transport")
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,null=True,blank=True)
    student = models.ForeignKey('student.Student',on_delete=models.SET_NULL,null=True,blank=True, related_name='fee_records')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    exams_type = models.CharField(max_length=50, choices=FEES_CHOICES)
    
    
    def __str__(self) -> str:
        if self.student:
            return f"{self.student.first_name} {self.student.last_name} - {self.exams_type}"
        elif self.user:
            return f"{self.user.username} - {self.exams_type}"
        else:
            return f"Fees #{self.pk} - {self.exams_type}"
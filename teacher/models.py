from django.db import models
from home_auth.models import CustomUser
import uuid


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    head_of_department = models.CharField(max_length=250)
    number_of_student = models.CharField(max_length=250)
    department_start_date = models.DateField()

    def __str__(self) -> str:
        return self.name


class Teacher(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("others", "Others"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department_id = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    mobile = models.CharField(max_length=250)
    qualification = models.CharField(max_length=250)
    experience = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    zipcode = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    joining_date = models.DateField()
    image = models.ImageField(upload_to="teachers/") 
    
    
   

    def __str__(self) -> str:
        return self.user.first_name


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=250)
    grade = models.IntegerField()

    def __str__(self) -> str:
        return self.name

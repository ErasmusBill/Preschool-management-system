from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Parent(models.Model):
    father_name=models.CharField(max_length=100)
    father_phone=models.CharField(max_length=15)
    father_occupation=models.CharField(max_length=100)
    father_email=models.EmailField()
    mother_name=models.CharField(max_length=100)
    mother_phone=models.CharField(max_length=15)
    mother_occupation=models.CharField(max_length=100)
    mother_email=models.EmailField()
    present_address = models.TextField()
    permanent_address = models.TextField()
    
    
    def __str__(self)->str:
        return f"{self.father_name} & {self.mother_name}"


class Student(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=100)
    religion = models.CharField(max_length=50)
    parent = models.OneToOneField(Parent, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    admission_number = models.CharField(max_length=20, unique=True)
    section = models.CharField(max_length=50)
    joining_date = models.DateField(auto_now_add=True)
    fees = models.ForeignKey('finance.Fees', on_delete=models.SET_NULL, blank=True, null=True, related_name='students_with_fees')
    mobile_number = models.CharField(max_length=15)
    student_image = models.ImageField(upload_to='student_images/', null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{self.first_name.lower()}-{self.last_name.lower()}-{self.student_id}"
        super(Student,self).save(*args, **kwargs)
        
        
    def validate_date_of_birth(self,date_of_birth):
        if date_of_birth > timezone.now():
            raise ValidationError("Date of birth cannot be in the future.")
    
    
    def __str__(self)-> str:
        return f"{self.first_name} {self.last_name}"

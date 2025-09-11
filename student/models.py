# student/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings

class Parent(models.Model):
    father_name = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=15)
    father_occupation = models.CharField(max_length=100)
    father_email = models.EmailField()
    mother_name = models.CharField(max_length=100)
    mother_phone = models.CharField(max_length=15)
    mother_occupation = models.CharField(max_length=100)
    mother_email = models.EmailField()
    present_address = models.TextField()
    permanent_address = models.TextField()

    def __str__(self) -> str:
        return f"{self.father_name} & {self.mother_name}"


class Student(models.Model):

    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )

    # Updated CLASS_CHOICES to include specific levels
    CLASS_CHOICES = [
        ("CRECHE", "Creche"),
        ("NURSERY_1", "Nursery 1"),
        ("NURSERY_2", "Nursery 2"),
        ("KINDERGARTEN", "Kindergarten"),
        ("UPPER_PRIMARY_4", "Upper Primary 4"),
        ("UPPER_PRIMARY_5", "Upper Primary 5"),
        ("UPPER_PRIMARY_6", "Upper Primary 6"),
        ("JHS_1", "JHS 1"),
        ("JHS_2", "JHS 2"),
        ("JHS_3", "JHS 3"),
    ]

    # Core User Link
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='student_profile',help_text="The user account associated with this student.")

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=100, choices=CLASS_CHOICES)
    religion = models.CharField(max_length=50)
    parent = models.OneToOneField(Parent, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # School Administration
    admission_number = models.CharField(max_length=20, unique=True)
    section = models.CharField(max_length=50)
    joining_date = models.DateField(auto_now_add=True)

    # Financial & Contact
    fees = models.ForeignKey('finance.Fees',on_delete=models.SET_NULL,blank=True,null=True,related_name='students_with_fees')
    mobile_number = models.CharField(max_length=15)
    student_image = models.ImageField(upload_to='student_images/', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def clean(self):
        """Model-level validation."""
        super().clean()
        if self.date_of_birth > timezone.now().date():
            raise ValidationError({'date_of_birth': "Date of birth cannot be in the future."})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.first_name} {self.last_name} {self.student_id}")
            self.slug = base_slug[:50]
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
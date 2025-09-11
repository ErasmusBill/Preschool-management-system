from django.db import models
from home_auth.models import CustomUser
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from student.models import Student


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
    image = models.ImageField(upload_to="teachers/", blank=True) 
    
    def __str__(self) -> str:
        return self.user.first_name


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=250)
    grade = models.IntegerField()

    def __str__(self) -> str:
        return self.name


class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student,on_delete=models.SET_NULL, null=True)
    assignment = models.FileField(upload_to="assignments/")  
    max_score = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    due_time = models.DateTimeField()

    def __str__(self):
        subject_name = self.subject.name if self.subject else "No Subject"
        teacher_name = self.teacher.user.first_name if self.teacher and self.teacher.user else "No Teacher"
        return f"{subject_name} - {teacher_name} ({self.start_time.date()} → {self.due_time.date()})"

class Grade(models.Model):
    GRADE_CHOICES = [
        ("A+", "A+ (90-100%)"),
        ("A", "A (80-89%)"),
        ("A-", "A- (75-79%)"),
        ("B+", "B+ (70-74%)"),
        ("B", "B (65-69%)"),
        ("B-", "B- (60-64%)"),
        ("C+", "C+ (55-59%)"),
        ("C", "C (50-54%)"),
        ("C-", "C- (45-49%)"),
        ("D+", "D+ (40-44%)"),
        ("D", "D (35-39%)"),
        ("F", "F (0-34%)"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_assignment = models.OneToOneField(
        Assignment, 
        on_delete=models.CASCADE,
        related_name='grade'
    )
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='grades_given'
    )
    letter_grade = models.CharField(choices=GRADE_CHOICES, max_length=2)
    numerical_score = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    remarks = models.TextField(max_length=1000, blank=True)  
    graded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-graded_at']
        verbose_name_plural = "Grades"

    def __str__(self):
        return f"{self.letter_grade} - {self.student_assignment}"

    def save(self, *args, **kwargs):
        # Auto-calculate letter grade based on numerical score
        if self.numerical_score is not None:
            if self.numerical_score >= 90:
                self.letter_grade = "A+"
            elif self.numerical_score >= 80:
                self.letter_grade = "A"
            elif self.numerical_score >= 75:
                self.letter_grade = "A-"
            elif self.numerical_score >= 70:
                self.letter_grade = "B+"
            elif self.numerical_score >= 65:
                self.letter_grade = "B"
            elif self.numerical_score >= 60:
                self.letter_grade = "B-"
            elif self.numerical_score >= 55:
                self.letter_grade = "C+"
            elif self.numerical_score >= 50:
                self.letter_grade = "C"
            elif self.numerical_score >= 45:
                self.letter_grade = "C-"
            elif self.numerical_score >= 40:
                self.letter_grade = "D+"
            elif self.numerical_score >= 35:
                self.letter_grade = "D"
            else:
                self.letter_grade = "F"
        
        super().save(*args, **kwargs)
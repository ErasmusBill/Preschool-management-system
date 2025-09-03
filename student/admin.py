from django.contrib import admin
from .models import Student,Parent
from django.contrib import admin
# Register your models here.






@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','student_id','student_class','date_of_birth','gender','admission_number','section','joining_date','mobile_number')
    search_fields = ('first_name','last_name','student_id','admission_number')
    list_filter = ('student_class','section','gender')



@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('father_name','father_phone','father_occupation','father_email','mother_name','mother_phone','mother_occupation','mother_email')
    search_fields = ('father_name','mother_name','father_phone','mother_phone')
    list_filter = ('father_name','mother_name')
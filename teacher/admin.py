from django.contrib import admin
from .models import *
from teacher.models import Subject

# Register your models here.
admin.site.register(Teacher)
admin.site.register(Department)
admin.site.register(Subject)

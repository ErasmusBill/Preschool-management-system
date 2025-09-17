from dataclasses import field
from django import forms
from .models import Assignment
from teacher.models import Assignment,Grade


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["assignment","subject","start_time","due_time","assignment_class","max_score"]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'due_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
        
class ResultForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["letter_grade","numerical_score","remarks"]
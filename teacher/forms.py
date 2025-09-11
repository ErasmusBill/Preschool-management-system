from django import forms
from .models import Assignment
from teacher.models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["assignment","subject","start_time","due_time","assignment_class","max_score"]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'due_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
from django import forms
from teacher.models import Enrollment   

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["student"]
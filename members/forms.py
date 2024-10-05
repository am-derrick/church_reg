from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    """Registration form utilising Django forms"""
    class Meta:
        model = Registration
        fields = ['first_name', 'last_name', 'gender', 'phone_number', 'residence',
                'is_student', 'is_first_time', 'consent']
        widgets = {
            'gender': forms.RadioSelect(choices=[('Male', 'Male'), ('Female', 'Female')]),
            'is_student': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'is_first_time': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'consent': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        }
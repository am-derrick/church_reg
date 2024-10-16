from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    """Registration form utilising Django forms"""
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    YES_NO_CHOICES = [('Yes', 'Yes'), ('No', 'No')]


    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    is_student = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    is_first_time = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
    consent = forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))


    class Meta:
        model = Registration
        fields = ['first_name', 'last_name', 'gender', 'phone_number', 'residence',
                'is_student', 'institution_name', 'institution_location', 'occupation',
                'is_first_time', 'consent']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Preferrably a number on WhatsApp', 'class': 'form-control'}),
            'residence': forms.TextInput(attrs={'placeholder': 'This is where you currently live i.e. City, Town, Estate, etc.', 'class': 'form-control'}),
            'institution_name': forms.TextInput(attrs={'placeholder': 'Enter institution name', 'class': 'form-control'}),
            'institution_location': forms.TextInput(attrs={'placeholder': 'Enter institution location', 'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'placeholder': 'Enter your occupation', 'class': 'form-control'}),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'gender': '',
            'phone_number': '',
            'residence': '',
            'is_student': '',
            'institution_name': '',
            'institution_location': '',
            'occupation': '',
            'is_first_time': '',
            'consent': '',
        }
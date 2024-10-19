from django import forms
from .models import Registration
    

class NameForm(forms.Form):
    """Form for Name fields"""
    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))

class RegistrationForm(forms.ModelForm):
    """Registration form utilising Django forms"""
    class Meta:
        model = Registration
        fields = ['first_name', 'last_name', 'gender', 'phone_number', 'residence',
                'is_student', 'institution_name', 'institution_location', 'occupation',
                'is_first_time', 'consent']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
            'gender': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
            'residence': forms.TextInput(attrs={'placeholder': 'This is where you currently live i.e. City, Town, Estate etc.',
                                                'class': 'form-control'}),
            'is_student': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'institution_name': forms.TextInput(attrs={'placeholder': 'Name of Institution', 'class': 'form-control'}),
            'institution_location': forms.TextInput(attrs={'placeholder': 'Location of Institution', 'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'placeholder': 'Occupation', 'class': 'form-control'}),
            'is_first_time': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'consent': forms.RadioSelect(attrs={'class': 'form-check-input'}),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'].choices = [('Male', 'Male'), ('Female', 'Female')]
        self.fields['is_student'].choices = [('Yes', 'Yes'), ('No', 'No')]
        self.fields['is_first_time'].choices = [('Yes', 'Yes'), ('No', 'No')]
        self.fields['consent'].choices = [('Yes', 'Yes'), ('No', 'No')]
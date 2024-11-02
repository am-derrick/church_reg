from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import Registration
from django.forms.widgets import Select, TextInput


class NameForm(forms.Form):
    """Form for Name fields"""

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "First Name", "class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name", "class": "form-control"}
        ),
    )


class RegistrationForm(forms.ModelForm):
    """Registration form utilising Django forms"""

    phone_number = PhoneNumberField(
        required=False,  # Make it optional
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. 0712345678 or +257712345678",
                "style": "width: 100%;",
            }
        ),
    )

    def clean_phone_number(self):
        """Custom validation for phone numbers"""
        phone_number = self.cleaned_data.get("phone_number")

        if not phone_number:
            return None

        # Convert the phone number to string for manipulation
        phone_str = str(phone_number)

        # Handle Kenyan numbers
        if phone_str.startswith("0"):  # Local format (0712345678)
            phone_str = "+254" + phone_str[1:]
        elif phone_str.startswith("254"):  # Without plus (254712345678)
            phone_str = "+" + phone_str
        elif not phone_str.startswith("+"):  # No country code
            phone_str = "+254" + phone_str

        try:
            from phonenumber_field.phonenumber import PhoneNumber

            return PhoneNumber.from_string(phone_str, region="KE")
        except Exception:
            raise forms.ValidationError("Please enter a valid phone number")

    class Meta:
        """Meta class details[columns]"""

        model = Registration
        fields = [
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "email",
            "residence",
            "is_student",
            "institution_name",
            "institution_location",
            "occupation",
            "is_first_time",
            "consent",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "First Name", "class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Last Name", "class": "form-control"}
            ),
            "gender": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Please enter a valid email ",
                    "class": "form-control",
                }
            ),
            "residence": forms.TextInput(
                attrs={
                    "placeholder": "This is where you currently live i.e. City, Town, Estate etc.",
                    "class": "form-control",
                }
            ),
            "is_student": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "institution_name": forms.TextInput(
                attrs={"placeholder": "Name of Institution", "class": "form-control"}
            ),
            "institution_location": forms.TextInput(
                attrs={
                    "placeholder": "Location of Institution",
                    "class": "form-control",
                }
            ),
            "occupation": forms.TextInput(
                attrs={"placeholder": "Occupation", "class": "form-control"}
            ),
            "is_first_time": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "consent": forms.RadioSelect(attrs={"class": "form-check-input"}),
        }
        labels = {
            "first_name": "",
            "last_name": "",
            "gender": "",
            "phone_number": "",
            "email": "",
            "residence": "",
            "is_student": "",
            "institution_name": "",
            "institution_location": "",
            "occupation": "",
            "is_first_time": "",
            "consent": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].choices = [("Male", "Male"), ("Female", "Female")]
        self.fields["is_student"].choices = [("Yes", "Yes"), ("No", "No")]
        self.fields["is_first_time"].choices = [("Yes", "Yes"), ("No", "No")]
        self.fields["consent"].choices = [("Yes", "Yes"), ("No", "No")]

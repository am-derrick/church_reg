from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Registration


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
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. 0712345678 or +257712345678",
                "style": "width: 100%;",
            }
        ),
        label="",
    )

    def __init__(self, *args, **kwargs):
        self.is_update = kwargs.pop("is_update", False)
        super().__init__(*args, **kwargs)
        self.fields["is_first_time"].choices = [("Yes", "Yes"), ("No", "No")]
        self.fields["consent"].choices = [("Yes", "Yes"), ("No", "No")]

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

            cleaned_phone = PhoneNumber.from_string(phone_str, region="KE")

            # For new registrations or if phone number is changing, check for uniqueness
            if not self.instance.pk or (
                self.instance.pk
                and str(cleaned_phone) != str(self.instance.phone_number)
            ):
                # Check if phone number is already in use by another registration
                existing = Registration.objects.filter(phone_number=cleaned_phone)
                if self.instance.pk:
                    existing = existing.exclude(pk=self.instance.pk)

                if existing.exists():
                    raise forms.ValidationError("This phone number is already in use.")

            return cleaned_phone

        except Exception as e:
            raise forms.ValidationError(f"Please enter a valid phone number: {str(e)}")

    class Meta:
        """Meta class details[columns]"""

        model = Registration
        fields = [
            "first_name",
            "last_name",
            "phone_number",
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
            "is_first_time": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "consent": forms.RadioSelect(attrs={"class": "form-check-input"}),
        }
        labels = {
            "first_name": "",
            "last_name": "",
            "phone_number": "",
            "is_first_time": "",
            "consent": "",
        }

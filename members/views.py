from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm, PhoneNumberForm
from .models import Registration

def registration_view(request):
    """Registration form view: displays registration form"""
    if request.method == 'POST':
        phone_form = PhoneNumberForm(request.POST)
        if phone_form.is_valid():
            phone_number = phone_form.cleaned_data['phone_number']
            try:
                registration = Registration.objects.get(phone_number=phone_number) # get phone number
                # Pre-fill form with existing data
                form = RegistrationForm(instance=registration)
                return render(request, 'registration_confirm.html', {'form': form, 'phone_number': phone_number})
            except Registration.DoesNotExist:
                # If user doesn't exist, show the full form
                form = RegistrationForm(initial={'phone_number': phone_number})
                return render(request, 'registration.html', {'form': form})
    else:
        phone_form = PhoneNumberForm()
    return render(request, 'phone_number.html', {'form': phone_form})

def registration_confirm(request):
        """Confrim or update existing registration"""
        if request.method == 'POST':
            phone_number = request.POST.get('phone_number')
            registration = Registration.objects.get(phone_number=phone_number)
            form = RegistrationForm(request.POST, instance=registration)
            if form.is_valid():
                registration = form.save()
                return redirect(reverse('welcome', kwargs={'first_name': registration.first_name}))
        return redirect('registration')

def welcome_view(request, first_name):
    """Thank you page view, displayed after registration"""
    return render(request, 'welcome.html', {'first_name': first_name})
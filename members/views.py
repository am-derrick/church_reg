from django.shortcuts import render, redirect
from .forms import RegistrationForm

def registration_view(request):
    """Registration form view: displays registration form"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save()
            return redirect('welcome', first_name=registration.first_name)
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def welcome_view(request, first_name):
    """Thank you page view, displayed after registration"""
    return render(request, 'welcome.html', {'first_name': first_name})
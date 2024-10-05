from django.shortcuts import render, redirect
from .forms import RegistrationForm


def registration_view(request):
    """Registration form view: displays registration form"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('welcome')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

def welcome_view(request):
    """Thank you page view, displayed after registration"""
    return render(request, 'welcome.html')
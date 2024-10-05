from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# from .models import MemberProfile
from .forms import RegistrationForm


def registration_view(request):
    """Registration form view: displays registration form"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

def thank_you_view(request):
    """Thank you page view, displayed after registration"""
    return render(request, 'thank_you.html')
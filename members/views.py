from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import MemberProfile


def registration_view(request):
    if request.method == 'POST':
        # to-do: handle form submission logic
        pass
    
    return render(request, 'members/registration.html')
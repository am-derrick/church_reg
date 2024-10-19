from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from .forms import RegistrationForm, NameForm
from .models import Registration

def registration_view(request):
    """Initial registration view: displays name form"""
    if request.method == 'POST':
        name_form = NameForm(request.POST)
        if name_form.is_valid():
            first_name = name_form.cleaned_data['first_name']
            last_name = name_form.cleaned_data['last_name']

            # Check if name exists in the db
            registration_data = Registration.objects.filter(
                Q(first_name__iexact=first_name) & Q(last_name__iexact=last_name))
            
            if registration_data.exists():
                # If name exists, render the confirmation page
                return render(request, 'name_confirmation.html', {
                    'first_name': first_name,
                    'last_name': last_name
                })
            else:
                # If name doesn't exist, show the full registration form
                form = RegistrationForm(initial={'first_name': first_name, 'last_name': last_name})
                return render(request, 'registration.html', {'form': form})
    else:
        name_form = NameForm()

    return render(request, 'name_form.html', {'form': name_form})


def registration_confirm(request):
        """Confrim existing registration or create new one"""
        if request.method == 'POST':
            action = request.POST.get('action')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if action == 'confirm':
                # User confirms their details and are redirected to welcome page
                return redirect(reverse('welcome', kwargs={'first_name': first_name}))
            elif action == 'update':
                # Fetch the existing registraion
                registration = Registration.objects.get(
                    Q(first_name__iexact=first_name) & Q(last_name__iexact=last_name)
                )
                form = RegistrationForm(instance=registration)
                return render(request, 'registration.html', {'form': form, 'is_update': True})
            elif action == 'new':
                # Start a new registration
                form = RegistrationForm(initial={'first_name': first_name, 'last_name': last_name})
                return render(request, 'registration.html', {'form': form})
            
        return redirect('register')


def registration_submit(request):
    """Handle registration form submission"""
    if request.method == 'POST':
        is_update = request.POST.get('is_update') == 'True'

        if is_update:
            registration = Registration.objects.get(
                Q(first_name__iexact=request.POST.get('first_name')) &
                Q(last_name__iexact=request.POST.get('last_name'))
            )
            form = RegistrationForm(request.POST, instance=registration)
        else:
            form = RegistrationForm(request.POST)

        if form.is_valid():
            registration = form.save()
            return redirect(reverse('welcome', kwargs={'first_name': registration.first_name}))
        else:
            # If form is not valid, re-render page with errors
            return render(request, 'registration.html', {'form': form, 'is_update': is_update})
    
    return redirect('register')


def welcome_view(request, first_name):
    """Thank you page view, displayed after registration"""
    return render(request, 'welcome.html', {'first_name': first_name})
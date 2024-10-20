from .utils import super_admin_required, admin_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.admin.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from members.models import Registration


User = get_user_model()

def login_view(request):
    """login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'custom_admin/login.html')

@login_required
def logout_view(request):
    """logout view"""
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    """view for the admin dashboard"""
    registrations = Registration.objects.all().order_by('-created_at')
    return render(request, 'custom_admin/admin_dashboard.html', {'registrations': registrations})

def user_list(request):
    """displays list for all users(admins)"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'custom_admin/user_list.html', {'users': users})

@admin_required
def user_create(request):
    """super user creates admins"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'custom_admin/user_form.html', {'form': form})

@admin_required
def user_edit(request, user_id):
    """super user edits users"""
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updates successfully.')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'custom_admin/user_form.html', {'form': form})

@super_admin_required
def user_deactivate(request, user_id):
    """super user deletes/deactivates other users"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, 'User deactivated succesfully.')
    return redirect('user_list')
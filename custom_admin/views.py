from .utils import get_page_range
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from datetime import datetime
from .utils import super_admin_required, admin_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
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
    """view for the admin dashboard with pagination"""
    order_by = request.GET.get('order_by', '-created_at')
    search_query = request.GET.get('search', '')
    date_range = request.GET.get('date_range', '')
    status_filter = request.GET.get('status', '')

    registrations = Registration.objects.all()

    # Search filter
    if search_query:
        registrations = registrations.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(residence__icontains=search_query) |
            Q(institution_name__icontains=search_query) |
            Q(occupation__icontains=search_query)
        )

    # Date range filter
    if date_range:
        try:
            start_date, end_date = date_range.split(' to ')
            start_date = datetime.strptime(start_date, '%d-%m-%Y')
            end_date = datetime.strptime(end_date, '%d-%m-%Y')
            end_date = end_date.replace(hour=23, minute=59, second=59) # Time components to ensure full day coverage
            registrations = registrations.filter(created_at__range=[start_date, end_date])
        except (ValueError, AttributeError):
            messages.error(request, 'Invalid date range format.')

    # Status filter
    if status_filter:
        if status_filter == 'student':
            registrations = registrations.filter(is_student=True)
        elif status_filter == 'first_time':
            registrations = registrations.filter(is_first_time=True)

    registrations = registrations.order_by(order_by)
    paginator = Paginator(registrations, 25)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    page_range = get_page_range(paginator, page_obj)

    context = {
        'registrations': page_obj,
        'order_by': order_by,
        'page_range': page_range,
        'search_query': search_query,
        'date_range': date_range,
        'status_filter': status_filter
    }

    return render(request, 'custom_admin/admin_dashboard.html', context )

@login_required
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
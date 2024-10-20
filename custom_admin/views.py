from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from members.models import Registration

class SignUpView(generic.CreateView):
    """sign up view created with Django generic views"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'custom_admin/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully. You can now log in.')
        return response

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

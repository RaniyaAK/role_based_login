from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, UserForm
from .models import Profile


# --- Register ---
def register(request):
    form = UserForm(request.POST or None)
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', '')

        # Step 1: Check if username exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists."

        # Step 1: Check if email exists
        if User.objects.filter(email=email).exists():
            error_message = "Email already exists."    

        # Step 2: Check if passwords match
        elif password != confirm_password:
            error_message = "Passwords do not match."

        # Step 3: Save user if no errors
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user, role=role)
            return redirect('login')

    return render(request, 'register.html', {
        'form': form,
        'error_message': error_message
    })


# --- Login ---
def user_login(request):
    form = LoginForm(request.POST or None)
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.profile.role == 'student':
                return redirect('student_dashboard')
            elif user.profile.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.profile.role == 'admin':
                return redirect('admin_dashboard')
        else:
            error_message = "Incorrect username or password."

    return render(request, 'login.html', {
        'form': form,
        'error_message': error_message
    })


# --- Dashboards ---
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')


@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')


# --- Logout ---
def user_logout(request):
    logout(request)
    return redirect('login')

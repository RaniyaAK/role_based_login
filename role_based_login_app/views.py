from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserForm
from .models import Profile
from django.contrib.auth.models import User


# --- Register ---
from django.contrib.auth.models import User

def register(request):
    form = UserForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        confirm_password = form.cleaned_data['confirm_password']  # make sure your form has this field

        # 1️⃣ Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'form': form,
                'error_message': 'Username already exists.'
            })

        # 2️⃣ Check if passwords match
        if password != confirm_password:
            return render(request, 'register.html', {
                'form': form,
                'error_message': 'Passwords do not match.'
            })

        # 3️⃣ Save user if both checks pass
        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        # Save profile (role)
        role = form.cleaned_data.get('role')
        Profile.objects.create(user=user, role=role)

        return redirect('login')

    return render(request, 'register.html', {'form': form})



# --- Login ---
def user_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.profile.role == 'student':
                return redirect('student_dashboard')
            elif user.profile.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.profile.role == 'admin':
                return redirect('admin_dashboard')
        else:
            # 🔴 Pass the error to the template
            return render(request, 'login.html', {
                'form': form,
                'error_message': 'Incorrect username or password.'
            })

    return render(request, 'login.html', {'form': form})

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
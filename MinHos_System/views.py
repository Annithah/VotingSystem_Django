from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm

# Home Page
def home(request):
    return render(request, 'MinHos_System/home.html')

# Admin Login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:  # Only admin
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials.')
    return render(request, 'MinHos_System/admin_login.html')

# Doctor Login
def doctor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_superuser:  # Only doctors (not admin)
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Invalid doctor credentials.')
    return render(request, 'MinHos_System/doctor_login.html')

# Admin Dashboard
@login_required
def admin_dashboard(request):
    return render(request, 'MinHos_System/admin_dashboard.html')

# Doctor Dashboard
@login_required
def doctor_dashboard(request):
    return render(request, 'MinHos_System/doctor_dashboard.html')

# Logout View
def logout_view(request): 
    logout(request)
    return redirect('home')

# Request Appointment View
def request_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'MinHos_System/request_appointment.html', {'message': 'Appointment requested successfully!', 'form': AppointmentForm()})
    else:
        form = AppointmentForm()
    return render(request, 'MinHos_System/request_appointment.html', {'form': form})

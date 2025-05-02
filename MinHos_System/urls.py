from django.urls import path
from django.http import HttpResponse
from .views import *


urlpatterns = [
    path('', home ),  # Home page
    path('admin_login/', admin_login, name='admin_login'),  # Admin login
    path('doctor_login/', doctor_login, name='doctor_login'),  # Doctor login
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'),  # Doctor dashboard
    path('logout/', logout_view, name='logout'),  # Logout
    path('request_appointment/', request_appointment, name='request_appointment'),  # Request appointment page
]


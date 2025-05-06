from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('vote/<int:candidate_id>/', views.vote, name='vote'),

    path('submit-comment/', views.submit_comment, name='submit_comment'),

]

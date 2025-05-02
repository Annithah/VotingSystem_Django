from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

"""
URL configuration for blogsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_view
from .import views
from django.contrib.auth import views as auth_views


# app_name = 'users'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_up/', views.author_signup_view, name='users-sign_up'),
    path('login/', auth_view.LoginView.as_view(template_name = 'users/login.html'), name='users-login'),
    path('logout/', auth_view.LogoutView.as_view(template_name = 'users/logout.html'), name='users-logout'),
    path('customer-home/', views.customerhome, name='blog-customer-home'),
    path('profile_form/', views.profile, name='users-profile'),
    path('edit_profile/', views.create_or_edit_profile, name='users-edit_profile'),
    path('author_info/<str:username>/', views.authorinfo, name='users-author_info'),
    path('admin-home/', views.admin_dashboard, name='blog-admin-home'),
    path('customers/', views.view_users, name='blog-customers'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

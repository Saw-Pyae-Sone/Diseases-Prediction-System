
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    # path('admin/', include('customadmin.urls')),
    path('adminlogin/', views.admin_login, name='admin_login'),  # Corrected URL name
    path('dashboard/', views.dashboard, name='dashboard'),  # Corrected URL name
    path('login/', views.login, name='login'),  # Corrected URL name
]
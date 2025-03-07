"""
URL configuration for p1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_reg/',admin_reg),
    path('medical_reg/',medical_reg),
    path('show_admins/',show_admins),
    path('show_medicals/',show_medicals),
    path('login/',login),
    path('logout/',logout),
    path('admin_home/',admin_home),
    path('medical_home/',medical_home),
    path('auth_error/',auth_error),
    path('edit_medical/',edit_medical),
    path('edit_medical1/',edit_medical1),
    path('delete_medical/',delete_medical),
    path('delete_medical1/', delete_medical1),
    path('medicine_reg/',medicine_reg),
    path('show_medicines/',show_medicines),
    path('',welcome),
    path('show_medicals_to_all/',show_medicals_to_all),
]

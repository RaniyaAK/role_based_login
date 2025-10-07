from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]


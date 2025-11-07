# akun/urls.py
from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView, 
    AkunListView,
    CurrentAkunView,
    AkunDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('akun/', AkunListView.as_view(), name='akun-list'),  # GET semua akun
    path('akun/me/', CurrentAkunView.as_view(), name='current-akun'),  # GET akun saat ini
    path('akun/<uuid:pk>/', AkunDetailView.as_view(), name='akun-detail'),  # GET akun by ID
]
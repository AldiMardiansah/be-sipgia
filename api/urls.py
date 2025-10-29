from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.get_data),
    path('save_user/', views.save_user),
]

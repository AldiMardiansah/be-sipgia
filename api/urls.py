from django.urls import path
from akun import views  # ⬅️ pakai views dari app akun

urlpatterns = [
    path('register/', views.register_api, name='register'),
    path('login/', views.login_api, name='login'),
    path('users/', views.user_list_api, name='user-list'),
]

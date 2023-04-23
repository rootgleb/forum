from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.register, name="signup"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
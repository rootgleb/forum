from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('topic/<int:pk>/', views.topic, name='topic'),
    path('user/<int:user_id>/', views.profile, name='profile'),
    path('add_post/', views.add_post, name="add"),
    path('categories/', views.category_page, name="categories"),
    path('categories/<int:category_id>/', views.category_posts, name="category_posts"),
    path('category/<int:pk>/', views.category, name='category'),
    path('rules/', views.rules, name='rules'),

]

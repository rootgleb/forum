from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('topic/<int:pk>/', views.topic, name='topic'),
    path('user/<int:user_id>/', views.profile, name='profile'),
    path('add_post/', views.add_post, name="add")
]

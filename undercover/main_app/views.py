from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .models import Post
from django.contrib.auth.models import User

def index(request):
    posts = reversed(Post.objects.order_by('date'))
    return render(request, "main_app/index.html", {"posts": posts})

def topic(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'main_app/topic.html', {'post': post})

def profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'profile.html', {'profile': user})
from django.contrib.auth import get_user_model


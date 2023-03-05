from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import PostForm
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


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('topic', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


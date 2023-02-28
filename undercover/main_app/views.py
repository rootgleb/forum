from django.shortcuts import render
from django.views.generic import ListView
from django.utils import timezone
from .models import Post




def index(request):
    posts = reversed(Post.objects.order_by('date'))
    print(posts)
    return render(request, "main_app/index.html", {"posts": posts})

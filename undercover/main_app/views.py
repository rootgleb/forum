from django.shortcuts import render, get_object_or_404
from .models import Post


def index(request):
    posts = reversed(Post.objects.order_by('date'))
    print(posts)
    return render(request, "main_app/index.html", {"posts": posts})

def topic(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'main_app/topic.html', {'post': post})


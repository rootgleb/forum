from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import PostForm, CommentForm
from .models import Post
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.order_by('date')[::-1]
    paginator = Paginator(posts, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main_app/index.html', {'page_obj': page_obj, "posts": posts})


def topic(request, pk):
    post = get_object_or_404(Post, pk=pk)

    comments = post.comments.all()

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.author = request.user
            # Save the comment to the database
            new_comment.save()
            return redirect('topic', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'main_app/topic.html', {'post': post,
                                                   'comments': comments,
                                                   "comment_form": comment_form})


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


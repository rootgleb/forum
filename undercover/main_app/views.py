from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import BanForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import PostForm, CommentForm
from .models import Post, Category
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect


def category_page(request):
    categories = Category.objects.filter(parent=None)

    def get_children(category):
        children = category.children.all()
        if children:
            for child in children:
                child.children.set(get_children(child))
        return children

    for category in categories:
        category.children.set(get_children(category))

    return render(request, "main_app/category.html", {'categories': categories})


def category_posts(request, category_id):
    category = Category.objects.get(id=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'category_posts.html', {'category': category, 'posts': posts})


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
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('topic', pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'main_app/topic.html', {'post': post,
                                                   'comments': comments,
                                                   "comment_form": comment_form})


def profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'profile.html', {'profile': user, 'user_id': user.id})


def add_post(request):
    user = request.user
    if request.method == 'POST':
        user = request.user
        form = PostForm(request.POST)

        if form.is_valid() and user.is_authenticated:
            profile = Profile.objects.get(user=user)
            if not profile.is_banned:
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('topic', pk=post.pk)
            else:
                return redirect(request, 'home')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

def category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category__in=category.get_descendants(include_self=True))
    paginator = Paginator(posts, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main_app/index.html', {'page_obj': page_obj, "posts": posts})

def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category__in=category.get_descendants(include_self=True))

    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'category.html', context)


def rules(request):
    return render(request, 'rules.html')

@login_required
def block_user(request, user_id):
    profile = get_object_or_404(Profile, pk=user_id)

    if request.method == 'POST':
        form = BanForm(request.POST)
        if form.is_valid() and request.user.is_staff:
            days = form.cleaned_data['days']
            months = form.cleaned_data['months']
            hours = form.cleaned_data['hours']
            years = form.cleaned_data['years']
            minutes = form.cleaned_data['minutes']
            reason = form.cleaned_data['reason']
            profile.ban(reason=reason, minutes=minutes, hours=hours, days=days, months=months, years=years)
            messages.success(request, f'{profile.user.username} заблокирован на {days} дня.')
            return redirect('profile', user_id=profile.user.id)
        if form.is_valid() and not request.user.is_staff:
            return render(request, "for_hacker.html")
    else:
        form = BanForm()

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'block_user.html', context)

@login_required
def unban_user(request, user_id):
    if request.user.is_staff:
        profile = get_object_or_404(Profile, pk=user_id)
        if not profile.is_banned:
            messages.error(request, 'This user is not banned.')
            return redirect('profile', user_id=profile.user.id)
        else:
            profile.is_banned = False
            profile.save()
            messages.success(request, 'User has been unbanned.')
            return redirect('profile', user_id=profile.user.id)
    else:
        return render(request, "for_hacker.html")

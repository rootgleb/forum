from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    category = TreeForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    url = models.TextField()

    def __str__(self):
        return self.title

    def __str__(self):
        return self.author.username


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name="Автор комментария", blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name="Текст комментария", max_length=2000)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    reputation = models.IntegerField(default=0)
    profile_image = models.ImageField()
    is_banned = models.BooleanField(default=False)
    ban_expiration_time = models.DateTimeField(null=True, blank=True)
    ban_reason = models.TextField(null=True, blank=True)

    def ban(self, years, months, days, hours, minutes, reason):
        self.is_banned = True
        self.ban_expiration_time = timezone.now() + timezone.timedelta(days=days + years * 365 + months * 30, hours=hours, minutes=minutes)
        self.ban_reason = reason
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


from django.shortcuts import render
from .models import Profile

class BanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Если пользователь заблокирован, перенаправляем на страницу ban_page.html
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
        if not request.user.is_authenticated:
            response = self.get_response(request)
            return response
        elif profile.is_banned:
            c = {
                'reason': profile.ban_reason,
                'time': profile.ban_expiration_time
            }
            return render(request, 'ban_page.html', context=c)
        else:
            response = self.get_response(request)
            return response
